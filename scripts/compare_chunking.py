import os
import time

import json
import numpy as np
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import (
    CharacterTextSplitter,
    NLTKTextSplitter,
    RecursiveCharacterTextSplitter,
)


def run_comparison():
    # Ensure docs directory exists
    os.makedirs("../docs", exist_ok=True)

    import nltk

    try:
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)
    except:
        pass

    loader = TextLoader("../data/resume.txt", encoding="utf-8")
    docs = loader.load()

    strategies = {
        "RecursiveCharacterTextSplitter": RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50
        ),
        "CharacterTextSplitter": CharacterTextSplitter(
            separator="\n\n", chunk_size=500, chunk_overlap=50
        ),
        "NLTKTextSplitter": NLTKTextSplitter(chunk_size=500),
    }

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    query = "What are Niranjan's main technical skills?"

    results = {}

    for name, splitter in strategies.items():
        try:
            splits = splitter.split_documents(docs)
            sizes = [len(split.page_content) for split in splits]

            num_chunks = len(splits)
            avg_size = float(np.mean(sizes)) if sizes else 0.0
            variance = float(np.var(sizes)) if sizes else 0.0

            # Test Retrieval
            start_time = time.time()
            vector_store = FAISS.from_documents(splits, embeddings)
            retriever = vector_store.as_retriever(search_kwargs={"k": 3})
            retrieved_docs = retriever.invoke(query)
            retrieval_time = time.time() - start_time

            results[name] = {
                "total_chunks": num_chunks,
                "average_chunk_size_chars": avg_size,
                "size_variance": variance,
                "retrieval_time_seconds": retrieval_time,
                "top_retrieved_snippet": (
                    retrieved_docs[0].page_content[:150] + "..."
                    if retrieved_docs
                    else None
                ),
            }
        except Exception as e:
            results[name] = {"error": str(e)}

    with open("../docs/chunking_strategy.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(
        "Chunking comparison complete. Results saved to ../docs/chunking_strategy.json"
    )


if __name__ == "__main__":
    run_comparison()
