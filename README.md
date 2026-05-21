# Ask About Me — Resume Q&A Engine

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-FF4B4B.svg?logo=Streamlit)](https://streamlit.io)
[![Azure AI Foundry](https://img.shields.io/badge/Azure%20AI-Foundry-0078D4.svg?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Live Demo**: [ask-about-niranjan-hebli.streamlit.app](https://ask-about-niranjan-hebli.streamlit.app/)

A premium, Google-like search engine interface built with **Streamlit** that allows recruiters to ask professional questions about me. The application queries an Azure AI Foundry project deployment model directly, utilizing documents that are uploaded and indexed in your Azure workspace.

---

## Features

- **Google Search UI**: A custom homepage logo, rounded search bar with autocomplete suggestions, interactive query tags, and a search results layout.
- **Featured AI Snippet**: Directly displays context-aware answers returned by Azure AI Foundry at the top of the search results page.
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