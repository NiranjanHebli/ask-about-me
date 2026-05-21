import time
import json
import requests
from config import (
    AZURE_ENDPOINT,
    AZURE_API_KEY,
    AZURE_MODEL_NAME,
    AZURE_AGENT_NAME,
    AZURE_AGENT_VERSION
)

def generate_mock_response(question):
    """Generates a mock response for Sandbox/Demo Mode."""
    q = question.lower()

    if any(k in q for k in ["skill", "stack", "technology", "programming", "languages"]):
        return (
            "Based on Niranjan Hebli's profile details, his technical skills include:\n\n"
            "• **Programming Languages:** Python, JavaScript, HTML5, CSS3, SQL\n"
            "• **AI/GenAI Frameworks:** LangGraph, LangChain, OpenAI API, Azure AI Foundry, LLM Orchestration, RAG (Retrieval-Augmented Generation)\n"
            "• **Backend & Databases:** Flask, FastAPI, Node.js, Express, PostgreSQL, MongoDB, Redis\n"
            "• **Tools & DevOps:** Git, Docker, Azure DevOps, VS Code"
        )
    elif any(k in q for k in ["experience", "work", "job", "career", "history"]):
        return (
            "Niranjan has been working as a **Generative AI Developer / Software Engineer** since May 2024. "
            "His main focus areas include:\n\n"
            "• Architecting and implementing multi-agent reasoning graphs using **LangGraph**.\n"
            "• Setting up advanced **RAG pipelines** for context-aware querying.\n"
            "• Building scalable backend services using **Flask** and **FastAPI**.\n"
            "• Automating data extraction and intelligence pipelines."
        )
    elif any(k in q for k in ["project", "build", "developed", "portfolio"]):
        return (
            "Niranjan has developed several notable projects:\n\n"
            "1. **Agentic Q&A System:** Multi-agent retrieval system using LangGraph with dynamic supervisor routing, specialized node endpoints, and self-validation loops. GitHub: [github.com/NiranjanHebli/agentic-qna-system](https://github.com/NiranjanHebli/agentic-qna-system)\n"
            "2. **NCERT Class IX Retrieval System:** Advanced retrieval and question-answering system for NCERT Class IX textbooks utilizing semantic chunking, metadata filtering, and custom RAG pipeline. GitHub: [github.com/NiranjanHebli/ncert-class-ix-retrieval-system](https://github.com/NiranjanHebli/ncert-class-ix-retrieval-system)\n"
            "3. **Churn Prediction AI:** Machine learning pipeline that processes customer behavioral data and predicts churn probability using scikit-learn and XGBoost. GitHub: [github.com/NiranjanHebli/churn-prediction-ai](https://github.com/NiranjanHebli/churn-prediction-ai)"
        )
    elif any(k in q for k in ["contact", "email", "phone", "reach", "linkedin", "github", "social"]):
        return (
            "You can contact Niranjan Hebli via:\n\n"
            "• **Email:** [niranjanhebli77@gmail.com](mailto:niranjanhebli77@gmail.com)\n"
            "• **GitHub:** [github.com/niranjanhebli](https://github.com/niranjanhebli)\n"
            "• **LinkedIn:** [linkedin.com/in/niranjan-hebli-333211211](https://www.linkedin.com/in/niranjan-hebli-333211211/)\n\n"
            "Feel free to reach out directly to coordinate interview schedules!"
        )
    elif any(k in q for k in ["education", "college", "degree", "university", "graduate"]):
        return (
            "Niranjan graduated in **2024** with a **Bachelor of Technology (B.Tech) in Computer Science and Engineering (CSE) from the National Institute of Technology Goa (NIT Goa)**."
        )
    else:
        return (
            "Niranjan Hebli is a Software Engineer and Generative AI Developer. He specializes in Python, GenAI frameworks like "
            "LangGraph and LangChain, and full-stack backend development.\n\n"
            "You can try searching:\n"
            "• What is Niranjan's tech stack?\n"
            "• Tell me about Niranjan's experience.\n"
            "• How can I contact Niranjan?\n"
            "• Tell me about his projects."
        )

def query_azure_ai_foundry(question):
    """Sends queries to Azure AI Foundry backend endpoint."""
    is_demo_mode = (
        not AZURE_API_KEY or
        not AZURE_ENDPOINT or
        "your_azure" in AZURE_API_KEY or
        "endpoint" in AZURE_ENDPOINT
    )

    if is_demo_mode:
        time.sleep(0.6)
        return generate_mock_response(question), "Local Demo Mode (No API keys configured)"

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY
    }

    url = AZURE_ENDPOINT.rstrip("/")
    if not (url.endswith("/chat/completions") or url.endswith("/responses")):
        if "/api/projects/" in url:
            if "/openai/v1" not in url:
                url += "/openai/v1/responses"
            else:
                url += "/responses"
        else:
            if url.endswith("/v1"):
                url += "/chat/completions"
            else:
                if "/v1" not in url:
                    url += "/v1/chat/completions"
                else:
                    url += "/chat/completions"

    system_instruction = (
        "You are an AI assistant representing Niranjan Hebli. "
        "Your task is to answer recruiter questions about Niranjan using the uploaded files and search tools available in this project connection. "
        "Keep your response professional, structured (with bullet points where appropriate), and concise."
    )

    if url.endswith("/responses"):
        payload = {
            "input": [
                {"role": "user", "content": question}
            ]
        }
        if AZURE_AGENT_NAME:
            payload["agent_reference"] = {
                "name": AZURE_AGENT_NAME,
                "version": AZURE_AGENT_VERSION,
                "type": "agent_reference"
            }
        else:
            payload["input"].insert(0, {"role": "system", "content": system_instruction})
    else:
        payload = {
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": question}
            ]
        }

    if AZURE_MODEL_NAME and not (url.endswith("/responses") and AZURE_AGENT_NAME):
        payload["model"] = AZURE_MODEL_NAME

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)

        if res.status_code in [401, 403]:
            headers["Authorization"] = f"Bearer {AZURE_API_KEY}"
            res = requests.post(url, json=payload, headers=headers, timeout=30)

        res.raise_for_status()
        res_data = res.json()

        content = None

        if "choices" in res_data and isinstance(res_data["choices"], list) and len(res_data["choices"]) > 0:
            choice = res_data["choices"][0]
            if isinstance(choice, dict):
                message = choice.get("message")
                if isinstance(message, dict) and "content" in message:
                    content = message["content"]
                elif isinstance(choice.get("delta"), dict) and "content" in choice["delta"]:
                    content = choice["delta"]["content"]
                elif "text" in choice:
                    content = choice["text"]

        if content is None and "output" in res_data:
            output_data = res_data["output"]

            if isinstance(output_data, list):
                text_parts = []
                for item in output_data:
                    if not isinstance(item, dict):
                        continue

                    contents = item.get("content")
                    if isinstance(contents, list):
                        for part in contents:
                            if isinstance(part, dict):
                                if part.get("type") == "output_text" and "text" in part:
                                    text_parts.append(str(part["text"]))
                                elif "text" in part:
                                    text_parts.append(str(part["text"]))
                    elif isinstance(contents, str):
                        text_parts.append(contents)
                    elif "text" in item:
                        text_parts.append(str(item["text"]))
                if text_parts:
                    content = "\n".join(text_parts)

            elif isinstance(output_data, dict):
                contents = output_data.get("content")
                if isinstance(contents, list):
                    text_parts = []
                    for part in contents:
                        if isinstance(part, dict) and "text" in part:
                            text_parts.append(str(part["text"]))
                    if text_parts:
                        content = "\n".join(text_parts)
                elif isinstance(contents, str):
                    content = contents
                elif "text" in output_data:
                    content = str(output_data["text"])

        if content is None:
            if "content" in res_data and isinstance(res_data["content"], str):
                content = res_data["content"]
            elif "response" in res_data and isinstance(res_data["response"], str):
                content = res_data["response"]

        if content is None:
            text_found = []
            def find_text_keys(obj):
                if isinstance(obj, dict):
                    if obj.get("role") == "user":
                        return
                    for k, v in obj.items():
                        if k == "text" and isinstance(v, str) and v.strip():
                            text_found.append(v)
                        else:
                            find_text_keys(v)
                elif isinstance(obj, list):
                    for item in obj:
                        find_text_keys(item)
            find_text_keys(res_data)
            if text_found:
                content = "\n".join(text_found)

        if content is None:
            content = json.dumps(res_data)

        return content, f"Azure AI Foundry ({AZURE_MODEL_NAME})"

    except requests.exceptions.HTTPError as e:
        status_code = res.status_code if 'res' in locals() else 'unknown'
        text_resp = res.text if 'res' in locals() else str(e)
        return (
            f"**Error querying Azure AI Foundry API (HTTP {status_code}):**\n"
            f"Endpoint: `{url}`\n\n"
            f"Details: `{text_resp}`\n\n"
            "Please check if the endpoint and API keys in your `.env` file are correct."
        ), "Error Status"
    except Exception as e:
        return f"**Failed to connect to Azure AI Foundry:** {str(e)}", "Connection Failure"
