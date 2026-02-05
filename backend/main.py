import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse, DocumentUploadResponse
from rag_engine import ingest_document, get_answer
from dotenv import load_dotenv
import anyio # For running sync functions in threads

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Run ingestion in a separate thread to avoid blocking the event loop
        print(f"Starting ingestion for {file.filename}...")
        num_chunks = await anyio.to_thread.run_sync(ingest_document, file_path)
        
        return {"filename": file.filename, "status": f"Successfully ingested {num_chunks} chunks."}
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Also run LLM call in a thread to keep the server responsive
        response = await anyio.to_thread.run_sync(get_answer, request.message, request.history)
        return {"answer": response, "sources": []}
    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

