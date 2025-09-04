# 📘 Smart Technical Document Assistant

A modern, RAG-powered GenAI assistant for querying technical documents (PDFs) with a beautiful futuristic UI.

## Features

- **RAG-Powered Technical Document Assistant**
  - Answers engineering and technical queries using uploaded documents.
  - Uses LangChain, ChromaDB, and Sentence-Transformers for retrieval and embeddings.
  - DeepSeek LLM via OpenRouter for high-quality answers.

- **Multi-PDF Upload**
  - Upload and process multiple PDF documents at once.
  - Supports large technical manuals, datasheets, and research papers.

- **Modern, Responsive UI**
  - Glassmorphism and neon design for a sleek look.
  - Mobile-friendly and fast.

- **Markdown Rendering**
  - Answers are rendered in markdown for better readability.
  - Supports code blocks, tables, and rich formatting.

- **Source Citation**
  - Each answer includes references to the source document and page number.

- **Document Management**
  - Add, remove, and update documents (if enabled).
  - Handles duplicate and missing files gracefully.

- **Fast, Local Vector Search**
  - Uses ChromaDB for efficient document chunk retrieval.

- **Easy Deployment**
  - Dockerfile and requirements.txt optimized for Railway and other cloud platforms.
  - Minimal image size for fast builds and low resource usage.

- **GitHub Ready**
  - Clean project structure, .gitignore, and .dockerignore included.

---

**Tech Stack:**  
Python 3.11+, Flask, LangChain, ChromaDB, Sentence-Transformers, DeepSeek (OpenRouter), markdown2, HTML/CSS

**How it works:**  
1. Upload PDFs  
2. Documents are chunked and embedded  
3. Ask questions—answers are generated using RAG and LLM  
4. Sources are cited for every answer

## Setup
1. Clone the repo and enter the directory:
   ```bash
   git clone <your-repo-url>
   cd ai-rag-agent
   ```
2. Create a Python virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add your OpenRouter API key to `.env`:
   ```
   OPENROUTER_API_KEY=sk-...
   ```
5. Run the app:
   ```bash
   python app.py
   ```
6. Open [http://localhost:5000](http://localhost:5000) in your browser.

## Usage
- Upload one or more technical PDFs.
- Ask questions about the documents.
- Get context-aware answers with source citations.

## Folder Structure
- `app.py` — main Flask app
- `pdf_loader.py` — PDF loading utility
- `templates/` — HTML templates (UI)
- `uploads/` — (ignored) uploaded files
- `.env` — (ignored) API keys

## Deployment
- Ready for HuggingFace Spaces, Streamlit Cloud, AWS, or Azure


