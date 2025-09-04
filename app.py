from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
import openai
import markdown2

load_dotenv()

app = Flask(__name__)

DB = None
VECTOR_CHUNKS = None

# Helper functions

def process_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(chunks, embeddings)
    return db, chunks

def ask_deepseek(query, context=None):
    api_key = os.getenv("OPENROUTER_API_KEY")
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": "You are a helpful assistant for technical documents."}
    ]
    if context:
        messages.append({"role": "system", "content": f"Context: {context}"})
    messages.append({"role": "user", "content": query})
    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3.1:free",
        messages=messages
    )
    return completion.choices[0].message.content

@app.route('/', methods=['GET', 'POST'])
def index():
    global DB, VECTOR_CHUNKS
    answer = None
    error = None
    uploaded_filenames = []
    if request.method == 'POST':
        if 'pdf' in request.files:
            pdf_files = request.files.getlist('pdf')
            all_documents = []
            filenames = []
            for pdf_file in pdf_files:
                pdf_path = os.path.join('uploads', pdf_file.filename)
                os.makedirs('uploads', exist_ok=True)
                pdf_file.save(pdf_path)
                filenames.append(pdf_file.filename)
                loader = PyPDFLoader(pdf_path)
                all_documents.extend(loader.load())
            uploaded_filenames = filenames
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(all_documents)
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            DB = Chroma.from_documents(chunks, embeddings)
            VECTOR_CHUNKS = chunks
        elif 'query' in request.form and DB and VECTOR_CHUNKS:
            query = request.form['query']
            retriever = DB.as_retriever(search_kwargs={"k": 3})
            docs = retriever.get_relevant_documents(query)
            context = "\n\n".join([doc.page_content for doc in docs])
            sources = []
            # Scan chunks for query keyword and cite only matching sources
            keyword = query.strip().split()[0] if query else None
            for doc in docs:
                if keyword and keyword.lower() in doc.page_content.lower():
                    meta = doc.metadata
                    source = meta.get('source', 'Unknown')
                    page = meta.get('page', 'N/A')
                    sources.append(f"{os.path.basename(source)} (Page {page})")
            if not sources and docs:
                # Fallback to top chunk if no match
                meta = docs[0].metadata
                source = meta.get('source', 'Unknown')
                page = meta.get('page', 'N/A')
                sources.append(f"{os.path.basename(source)} (Page {page})")
            try:
                raw_answer = ask_deepseek(query, context)
                answer = markdown2.markdown(raw_answer)
            except Exception as e:
                error = str(e)
    return render_template('index.html', answer=answer, error=error, uploaded_filenames=uploaded_filenames, sources=sources if 'sources' in locals() else None)

@app.route('/api/ask', methods=['POST'])
def api_ask():
    global DB, VECTOR_CHUNKS
    data = request.get_json()
    query = data.get('query')
    if not DB or not VECTOR_CHUNKS:
        return jsonify({'error': 'No document loaded.'}), 400
    retriever = DB.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    try:
        answer = ask_deepseek(query, context)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
