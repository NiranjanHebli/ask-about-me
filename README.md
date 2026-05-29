# Ask About Me — Resume Q&A Engine

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-FF4B4B.svg?logo=Streamlit)](https://streamlit.io)
[![Groq API](https://img.shields.io/badge/LLM-Groq-orange.svg)](https://groq.com/)
[![FAISS](https://img.shields.io/badge/VectorDB-FAISS-blue.svg)](https://github.com/facebookresearch/faiss)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Live Demo**: [ask-about-me-niranjan.streamlit.app](https://ask-about-me-niranjan.streamlit.app/)

A premium, Google-like search engine interface built with **Streamlit** that allows recruiters to ask professional questions about me. The application queries a model hosted on **Groq** using a local **FAISS** vector store populated by documents in the local workspace (like the candidate's resume).

---

## Features

- **Google Search UI**: A custom homepage logo, rounded search bar with autocomplete suggestions, interactive query tags, and a search results layout.
- **Featured AI Snippet**: Directly displays context-aware answers returned by Groq using local RAG context at the top of the search results page.
- **Knowledge Graph Sidebar**: Quick panel containing professional summaries, educational backgrounds, primary skill sets, and contact badges.
- **Floating Theme Controller**: A fixed-position light/dark mode switch at the top-right of the screen that dynamically applies dark/light styles persistently using a JavaScript MutationObserver.
- **Colorful Bouncing Loader**: A custom CSS-animated Google-colored bouncing dots loader that provides elegant visual feedback during model queries.
- **Optimized Performance**: Instant transitions with custom state-flushing to prevent page bleed and layout shifts during asynchronous model executions.

---


## Setup and Running Instructions

### 1. Install Dependencies
Make sure you have Python 3.9+ and `pip3` installed, then run:
```bash
pip3 install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the template to create your local environment file:
```bash
cp .env.example .env
```

### 3. Run the App
Start the Streamlit server:
```bash
streamlit run app.py
```
The interface should automatically open in your default browser at `http://localhost:8501`.

---

## Evaluation and Strategy Comparison

The repository contains scripts designed to evaluate and compare different text chunking and tokenization strategies, helping justify the architectural choices of our RAG pipeline.

### Running the Comparison Scripts

Since the evaluation scripts rely on relative path references to the source data and output documentation, they must be executed from within the `scripts` directory:

1. **Compare Chunking Strategies**:
   Runs a comparison across Recursive Character, separator-based Character, and NLTK-based splitters using FAISS retrieval speed and chunk size metrics.
   ```bash
   cd scripts
   python compare_chunking.py
   ```
   This saves raw benchmark results to [chunking_strategy.json](docs/chunking_strategy.json).

2. **Compare Tokenizers**:
   Compares Byte-Pair Encoding (BPE) and word tokenizers (Tiktoken `cl100k_base`, HuggingFace `gpt2`, and NLTK) for token counts, speeds, and compression efficiency.
   ```bash
   cd scripts
   python compare_tokenization.py
   ```
   This saves raw benchmark results to [tokenizer_strategy.json](docs/tokenizer_strategy.json).

For more details on the comparison scripts, see [compare_chunking.py](scripts/compare_chunking.py) and [compare_tokenization.py](scripts/compare_tokenization.py).

### Strategy Decisions & Rationale

To understand why these specific chunking sizes and tokenizer strategies are used in the main application pipeline, refer to the following architectural reflections:
- [Chunking Strategy Reflection](docs/chunking_strategy.md)
- [Tokenizer Strategy Reflection](docs/tokenizer_strategy.md)