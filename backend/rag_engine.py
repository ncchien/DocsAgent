import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Initialize Vector Store (Persistent)
PERSIST_DIRECTORY = "./chroma_db"

# Custom Embedding Configuration with Timeout
embedding_function = OpenAIEmbeddings(
    base_url="http://103.9.156.20:9000/v1",
    model="bge-m3:latest",
    api_key="sk-no-key-required",
    check_embedding_ctx_length=False,
    timeout=30.0, # Reasonable timeout for production
    max_retries=2 # Allow some retries for robustness
)

vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding_function)

def ingest_document(file_path: str):
    """Loads a PDF, splits it, and adds it to the vector store."""
    try:
        print(f"Loading document: {file_path}")
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} pages.")
        
        # Text splitter optimized for BGE-M3 (supports larger context, but we keep chunks manageable)
        print("Splitting text...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)
        print(f"Created {len(splits)} splits.")
        
        print("Adding to vector store (this might take a while if embeddings are slow)...")
        vectorstore.add_documents(documents=splits)
        print("Vector store update complete.")
        return len(splits)
    except Exception as e:
        print(f"Error during ingestion: {str(e)}")
        # Re-raise to be caught by the API handler
        raise Exception(f"Failed to process document: {str(e)}")

def get_answer(question: str, history: List[dict] = []):
    """Retrieves context and generates an answer."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    # RAG Prompt
    template = """You are a helpful product documentation assistant. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Custom LLM Configuration with Timeout
    llm = ChatOpenAI(
        base_url="http://103.9.156.20:80/v1",
        model_name="medgemma-27b-it",
        temperature=0,
        api_key="sk-no-key-required",
        request_timeout=60.0 # Add timeout for LLM
    )
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain.invoke(question)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
