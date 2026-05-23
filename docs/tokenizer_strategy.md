# Tokenizer Strategy Reflection

Our project relies on two tokenization strategies depending on the layer of the pipeline: one for **Retrieval (Embeddings)** and one for **Generation (LLM)**.

## 1. Retrieval: `all-MiniLM-L6-v2` Tokenizer
When storing chunks in our FAISS vector database, we use the `sentence-transformers` library, which automatically invokes the native subword tokenizer tied to the `all-MiniLM-L6-v2` model.
- **Rationale:** It is absolutely mandatory to use the exact tokenizer an embedding model was trained on to achieve valid vector embeddings. Since the model has a strict context limit of 256 tokens, utilizing its native tokenizer guarantees we align token boundaries correctly and prevent any truncation of meaning before hitting the vector store.

## 2. Generation: Groq LLM Tokenizer (Llama 3 / cl100k_base equivalents)
When passing the retrieved chunks as context to the Groq LLM, the text is tokenized by the LLM's own Byte-Pair Encoding (BPE) tokenizer.
- **Rationale:** Modern BPE tokenizers like Tiktoken (`cl100k_base`) or Llama 3's tokenizer possess massive vocabularies (~128k unique tokens). They have extremely high *token density*, meaning they can encode more text into fewer tokens. This is crucial for our project because it reduces API inference costs on Groq and preserves more available space in the LLM context window for our complex system instructions.
