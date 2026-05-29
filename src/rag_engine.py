import os
import threading

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

FAISS_INDEX_PATH = "data/faiss_index"

_embeddings = None
_vector_store = None
_lock = threading.RLock()


def get_embeddings():
    global _embeddings
    with _lock:
        if _embeddings is None:
            _embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings


def get_vector_store():
    """Initializes and returns the FAISS vector store. Builds it if it doesn't exist."""
    global _vector_store
    with _lock:
        if _vector_store is not None:
            return _vector_store

        embeddings = get_embeddings()
        if os.path.exists(FAISS_INDEX_PATH):
            _vector_store = FAISS.load_local(
                FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True
            )
            return _vector_store

        # Load document
        resume_path = "data/resume.txt"
        if not os.path.exists(resume_path):
            raise FileNotFoundError(f"Resume data not found at {resume_path}")

        loader = TextLoader(resume_path, encoding="utf-8")
        docs = loader.load()

        # Chunking using Recursive Character strategy as default
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)

        # Embed and store
        _vector_store = FAISS.from_documents(splits, embeddings)
        _vector_store.save_local(FAISS_INDEX_PATH)
        return _vector_store


def retrieve_context(query: str, k: int = 3) -> str:
    """Retrieves relevant text chunks from the vector database for a given query."""
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    return context
