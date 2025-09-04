# 📘 Smart Technical Document Assistant

A modern, RAG-powered GenAI assistant for querying technical documents (PDFs) with a beautiful futuristic UI.

## Features
- Multi-PDF upload and semantic search
- RAG pipeline: PDF loader, text splitter, vector DB (Chroma), LLM (DeepSeek via OpenRouter)
- Source citation: shows document and page for each answer
- Markdown-formatted answers
- Glassmorphism, glowing, and responsive UI

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

## License
MIT
