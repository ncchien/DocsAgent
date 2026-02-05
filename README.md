# Product Documentation Agent

A RAG (Retrieval-Augmented Generation) based application to chat with product documentation.

## Features
- PDF Document Upload and Ingestion
- AI Chat Interface with Contextual Awareness
- Robust Error Handling and Timeouts

## Tech Stack
- **Backend**: FastAPI, LangChain, ChromaDB, OpenAI/HuggingFace (via API)
- **Frontend**: React (Vite), Tailwind CSS, Lucide React

## Getting Started

### Backend
1. Navigate to `backend/`
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file with your keys
5. Run the server: `python -m uvicorn main:app --reload`

### Frontend
1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`
