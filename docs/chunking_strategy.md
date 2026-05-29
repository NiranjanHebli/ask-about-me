# Chunking Strategy Reflection

For this RAG pipeline, we have selected the **RecursiveCharacterTextSplitter** with a chunk size of 500 characters and an overlap of 50 characters.

## Rationale

1. **Preserving Context Boundaries:** 
Unlike the standard `CharacterTextSplitter` which strictly breaks on single separators (like `\n\n`), the `RecursiveCharacterTextSplitter` attempts to break on paragraphs, then sentences, then words. This hierarchal approach ensures that chunks remain semantically cohesive, minimizing the risk of splitting a core thought in half.

2. **Compatibility with Embedding Model:** 
Our embedding model, `all-MiniLM-L6-v2`, has a maximum context window of 256 tokens. A chunk size of 500 characters translates roughly to 100-130 tokens. This keeps us safely within the limits of the embedding model, completely avoiding truncation errors during FAISS indexing.

3. **Retrieval Efficiency:** 
A 500-character chunk strikes a perfect balance. It provides enough surrounding context for the generative LLM (Groq) to formulate an accurate answer, without injecting so much noise that the LLM loses focus on the specific user prompt. The 50-character overlap ensures that concepts split across chunk boundaries aren't entirely lost.
