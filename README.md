# FastAPI RAG Chatbot

A lightweight RAG (Retrieval-Augmented Generation) chatbot API built with FastAPI, LangChain, and Hugging Face Transformers.

Features

- Retrieves relevant documents using BAAI/bge-large-en embeddings.
- Generates grounded answers via HuggingFaceH4/zephyr-7b-beta.
- Provides chat, history, and analysis endpoints.

Modular and production-ready FastAPI structure.
- Python + FastAPI + Pydantic

Requirements
- Python 3.8+
- Install dependencies:
  pip install fastapi uvicorn

Run
- Start the app:
  uvicorn main:app --reload --port 8000
