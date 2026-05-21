"""pdf_generator.py — Generates a formatted PDF resume for Niranjan Hebli."""

from fpdf import FPDF


def generate_resume_pdf() -> bytes:
    """Builds and returns a professionally formatted PDF resume as bytes."""

    pdf = FPDF()
    pdf.set_margins(22, 22, 22)
    pdf.add_page()
    page_w = pdf.w - pdf.l_margin - pdf.r_margin  # usable width

    # Header
    pdf.set_font("helvetica", style="B", size=26)
    pdf.set_text_color(15, 15, 30)
    pdf.cell(page_w, 12, "Niranjan Hebli", new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.set_font("helvetica", size=11)
    pdf.set_text_color(80, 80, 110)
    pdf.cell(page_w, 7, "Generative AI Developer  &  Software Engineer", new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.set_font("helvetica", size=9)
    pdf.set_text_color(120, 120, 150)
    pdf.cell(page_w, 6, "github.com/niranjanhebli   |   linkedin.com/in/niranjan-hebli-333211211   |   niranjanhebli77@gmail.com", new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.ln(4)
    pdf.set_draw_color(200, 200, 220)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + page_w, pdf.get_y())
    pdf.ln(7)

    # Helpers
    def section(title: str):
        pdf.set_font("helvetica", style="B", size=10)
        pdf.set_text_color(40, 40, 80)
        pdf.cell(page_w, 7, title.upper(), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(180, 180, 210)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + page_w, pdf.get_y())
        pdf.ln(4)

    def body(text: str, indent: float = 0):
        pdf.set_font("helvetica", size=10)
        pdf.set_text_color(50, 50, 70)
        pdf.set_x(pdf.l_margin + indent)
        pdf.multi_cell(page_w - indent, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    def job_title(title: str, period: str):
        pdf.set_font("helvetica", style="B", size=10)
        pdf.set_text_color(20, 20, 50)
        pdf.cell(page_w, 7, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", style="I", size=9)
        pdf.set_text_color(110, 110, 140)
        pdf.cell(page_w, 5, period, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    # Summary
    section("Professional Summary")
    body(
        "Software Engineer and Generative AI Developer specializing in LLM orchestration, "
        "multi-agent systems, and RAG pipelines. Experienced in building scalable backend "
        "services and intelligent AI applications using Python and modern AI frameworks "
        "such as LangGraph, LangChain, and Azure AI Foundry."
    )
    pdf.ln(4)

    # Experience
    section("Experience")
    job_title("Generative AI Developer / Software Engineer", "May 2024 - Present")

    bullets = [
        "Architected multi-agent reasoning graphs using LangGraph for intelligent query routing.",
        "Set up advanced RAG pipelines for context-aware document querying and knowledge retrieval.",
        "Built scalable REST API backend services using Flask and FastAPI.",
        "Automated data extraction and intelligence pipelines with Python.",
        "Integrated Azure AI Foundry deployments for enterprise AI solutions.",
    ]
    for b in bullets:
        body(f"- {b}", indent=5)
    pdf.ln(4)

    # Education
    section("Education")
    job_title("Bachelor of Technology in Computer Science and Engineering", "National Institute of Technology Goa (NIT Goa)  |  Graduated 2024")
    pdf.ln(4)

    # Skills
    section("Technical Skills")
    skills = [
        ("Languages",    "Python, JavaScript, HTML5, CSS3, SQL"),
        ("AI / GenAI",   "LangGraph, LangChain, OpenAI API, Azure AI Foundry, RAG, LLM Orchestration"),
        ("Backend",      "Flask, FastAPI, Node.js, Express"),
        ("Databases",    "PostgreSQL, MongoDB, Redis"),
        ("Tools",        "Git, Docker, Azure DevOps, VS Code"),
    ]
    for label, value in skills:
        pdf.set_font("helvetica", style="B", size=10)
        pdf.set_text_color(30, 30, 60)
        pdf.set_x(pdf.l_margin)
        pdf.cell(32, 6, f"{label}:", new_x="RIGHT", new_y="TOP")
        pdf.set_font("helvetica", size=10)
        pdf.set_text_color(50, 50, 70)
        pdf.multi_cell(page_w - 32, 6, value, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Projects
    section("Notable Projects")
    projects = [
        (
            "Agentic Q&A System",
            "Multi-agent retrieval system using LangGraph with dynamic supervisor routing, "
            "specialized node endpoints, and self-validation loops. GitHub: github.com/NiranjanHebli/agentic-qna-system",
        ),
        (
            "NCERT Class IX Retrieval System",
            "Advanced retrieval and question-answering system for NCERT Class IX textbooks "
            "utilizing semantic chunking, metadata filtering, and custom RAG pipeline. GitHub: github.com/NiranjanHebli/ncert-class-ix-retrieval-system",
        ),
        (
            "Churn Prediction AI",
            "Machine learning pipeline that processes customer behavioral data and predicts "
            "churn probability using scikit-learn and XGBoost. GitHub: github.com/NiranjanHebli/churn-prediction-ai",
        ),
    ]
    for name, desc in projects:
        pdf.set_font("helvetica", style="B", size=10)
        pdf.set_text_color(20, 20, 50)
        pdf.cell(page_w, 7, name, new_x="LMARGIN", new_y="NEXT")
        body(desc, indent=5)
        pdf.ln(1)

    return bytes(pdf.output())
