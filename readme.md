
##################################################################################
##################################################################################

## WRYD Assignment – RAG-Based AI System

# 📌 Project Overview

This project implements an end-to-end Retrieval-Augmented Generation (RAG) pipeline.
The system scrapes website content, stores it in a vector database, and uses a local LLM to answer user queries strictly based on retrieved context.

# 🛠️ Tech Stack

- Web Scraping: Playwright
- Embeddings Model: nomic-embed-text (via Ollama)
- Vector Database: Chroma (persistent storage)
- LLM Framework: LangChain
- LLM Model: llama3:latest (via Ollama)

# ⚙️ Architecture Workflow

Scraping
The complete website content is scraped using Playwright.

Text Processing

Content is cleaned

Split into chunks using RecursiveCharacterTextSplitter

Embedding Generation

Each chunk is converted into vector embeddings using nomic-embed-text

Vector Storage

Embeddings are stored in a persistent Chroma database

Retrieval + Generation

LangChain retrieves the most relevant chunks

llama3:latest generates answers strictly using retrieved context


# to run the project

install all requirements.txt
then run llm.py 
then run main.py

# scrrenshots









