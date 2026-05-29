# Research: Evaluating Chunking Strategies & Tokenizers

Evaluating Retrieval-Augmented Generation (RAG) pipelines involves looking closely at how text is chunked and how those chunks are tokenized. This research document outlines the key metrics and methodologies used to evaluate these two foundational components.

---

## Metrics for Evaluating Chunking Strategies

Evaluating chunking is typically split into three layers: Retrieval Quality, Generation Quality, and Operational Efficiency. Tools like **RAGAS** and **TruLens** (using LLM-as-a-judge) are industry standards for measuring these.

### A. Retrieval Metrics (Search Quality)
These metrics determine if your chunking strategy is helping the vector database find the *right* information.
- **Recall@k:** The percentage of queries where the relevant chunk (containing the ground truth answer) is retrieved within the top *k* results. Low recall means chunks might be truncating necessary context.
- **Precision@k:** The proportion of retrieved chunks that are actually relevant to the query. Low precision indicates chunks might be too large, pulling in "noise" and distracting the LLM.
- **Mean Reciprocal Rank (MRR):** Measures how high up the results list the first relevant chunk appears.
- **Token-wise Intersection over Union (IoU):** Measures the token overlap between the retrieved chunk and the exact ground truth context.

### Generation Metrics (LLM Output Quality)
These metrics evaluate how the retrieved chunks impact the final LLM response.
- **Faithfulness (Groundedness):** Measures whether the generated answer is derived *exclusively* from the retrieved context. Poor chunking (e.g., splitting a sentence in half) often leads to hallucinations.
- **Answer Relevancy:** Measures how pertinent the final answer is to the user's original query.
- **Context Relevancy:** Evaluates if the retrieved chunks actually contain the information needed to answer the query.

###  Operational & Efficiency Metrics
These metrics track the cost and performance impact of the chunking strategy.
- **Retrieval/Generation Latency:** Time taken to embed, search, and generate. Complex semantic chunking might increase upfront latency.
- **Token Usage / Cost:** Larger chunks consume more context window space, increasing API costs.
- **Chunk Count & Size Variance:** Measures the consistency of your chunks. High variance might indicate unpredictable retrieval behavior.

---

##  Metrics for Evaluating Tokenizers

While tokenizers are usually fixed to the embedding model (e.g., `sentence-transformers` for `all-MiniLM-L6-v2`) and the generative LLM (e.g., `tiktoken` for OpenAI, `Llama 3 Tokenizer` for Groq), understanding their efficiency is crucial.

### A. Token Density (Tokens per Character/Word)
- **What it is:** The ratio of tokens generated relative to the original text length.
- **Why it matters:** A highly efficient tokenizer (like `cl100k_base` or Llama 3's BPE) uses fewer tokens to represent the same text. This allows you to fit more actual text (context) into the LLM's fixed context window and reduces API costs.

### B. Vocabulary Size & Out-of-Vocabulary (OOV) Rate
- **What it is:** The number of unique tokens the tokenizer knows, and how often it fails to recognize a word.
- **Why it matters:** Modern BPE (Byte-Pair Encoding) tokenizers have virtually 0% OOV rate because they fall back to byte-level encoding. A larger vocabulary (e.g., Llama 3's 128k vocab) generally leads to better token density.

### C. Encoding / Decoding Latency
- **What it is:** The computational speed of converting raw string text to token integer arrays and back.
- **Why it matters:** For real-time applications and massive data ingestion pipelines, tokenizer speed (often written in Rust, like `tiktoken`) reduces processing bottlenecks.

### D. Semantic Boundary Alignment
- **What it is:** How well the token boundaries align with actual morphological boundaries (prefixes, root words, suffixes).
- **Why it matters:** Better semantic alignment helps embedding models (like `all-MiniLM-L6-v2`) capture the true meaning of the text without getting confused by arbitrary character splits.

---

## Best Practices

1. **Embedding Alignment:** Your chunking strategy must respect the maximum token limit of your embedding model. For `all-MiniLM-L6-v2`, the limit is typically 256 or 512 tokens. Our current fixed-size chunking of 500 characters easily fits within this limit.

2. **Testing Workflow:** To find the optimal strategy, establish a "Golden Dataset" of Q&A pairs. Run a sweep of different chunk sizes (e.g., 250, 500, 1000 characters) and evaluate them using Retrieval Metrics (Recall/Precision) and Generation Metrics (Faithfulness).
