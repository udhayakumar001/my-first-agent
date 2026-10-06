from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ── Page margins ──────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin   = Cm(2.5)
    section.right_margin  = Cm(2.5)

# ── Color palette ─────────────────────────────────────────────
DARK_BG  = RGBColor(0x1E, 0x1E, 0x2E)
ACCENT   = RGBColor(0x74, 0xC7, 0xEC)
GOLD     = RGBColor(0xF9, 0xE2, 0xAF)
CODE_FG  = RGBColor(0xCD, 0xD6, 0xF4)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
MUTED    = RGBColor(0xA6, 0xAD, 0xC8)
GREEN    = RGBColor(0xA6, 0xE3, 0xA1)
RED_SOFT = RGBColor(0xFF, 0x88, 0x88)


def shd(para, fill_hex):
    pPr = para._p.get_or_add_pPr()
    s = OxmlElement('w:shd')
    s.set(qn('w:val'),   'clear')
    s.set(qn('w:color'), 'auto')
    s.set(qn('w:fill'),  fill_hex)
    pPr.append(s)


def cell_shd(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement('w:shd')
    s.set(qn('w:val'),   'clear')
    s.set(qn('w:color'), 'auto')
    s.set(qn('w:fill'),  fill_hex)
    tcPr.append(s)


def rc(run, rgb):
    run.font.color.rgb = rgb


def heading1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    shd(p, '1E1E2E')
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(6)
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(20)
    rc(r, ACCENT)


def heading2(doc, text):
    p = doc.add_paragraph()
    shd(p, '31314A')
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(3)
    r = p.add_run(f"  {text}")
    r.bold = True; r.font.size = Pt(13)
    rc(r, GOLD)


def step_heading(doc, num, title):
    p = doc.add_paragraph()
    shd(p, '313244')
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(3)
    rn = p.add_run(f"  STEP {num}  ")
    rn.bold = True; rn.font.size = Pt(11)
    rPr = rn._r.get_or_add_rPr()
    s = OxmlElement('w:shd')
    s.set(qn('w:val'),'clear'); s.set(qn('w:color'),'auto'); s.set(qn('w:fill'),'74C7EC')
    rPr.append(s)
    rc(rn, DARK_BG)
    rt = p.add_run(f"  {title}")
    rt.bold = True; rt.font.size = Pt(12)
    rc(rt, WHITE)


def body(doc, text, color=None):
    p = doc.add_paragraph()
    shd(p, '1E1E2E')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.font.size = Pt(10.5)
    rc(r, color or MUTED)


def bullet(doc, text, color=None):
    p = doc.add_paragraph()
    shd(p, '1E1E2E')
    p.paragraph_format.left_indent  = Inches(0.3)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(1)
    r = p.add_run(f"  o  {text}")
    r.font.size = Pt(10.5)
    rc(r, color or MUTED)


def code(doc, lines):
    for line in lines:
        p = doc.add_paragraph()
        shd(p, '282838')
        p.paragraph_format.left_indent  = Inches(0.2)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(0)
        r = p.add_run(line if line else " ")
        r.font.name = "Courier New"
        r.font.size = Pt(9)
        rc(r, CODE_FG)


def divider(doc):
    p = doc.add_paragraph()
    shd(p, '1E1E2E')
    r = p.add_run("-" * 100)
    rc(r, RGBColor(0x45, 0x47, 0x5A))
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(6)


def note_box(doc, text, fill='313244', color=None):
    p = doc.add_paragraph()
    shd(p, fill)
    p.paragraph_format.left_indent  = Inches(0.2)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run(f"  {text}")
    r.font.size = Pt(10)
    r.italic = True
    rc(r, color or GOLD)


# ==============================================================
# COVER
# ==============================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
shd(p, '1E1E2E')
p.paragraph_format.space_before = Pt(30)
p.paragraph_format.space_after  = Pt(4)
r = p.add_run("my-first-agent")
r.bold = True; r.font.size = Pt(34); rc(r, ACCENT)

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
shd(p2, '1E1E2E')
p2.paragraph_format.space_after = Pt(2)
r2 = p2.add_run("Complete Project Guide | Step-by-Step Procedure & Source Code")
r2.font.size = Pt(12); r2.italic = True; rc(r2, MUTED)

p3 = doc.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
shd(p3, '1E1E2E')
p3.paragraph_format.space_after = Pt(20)
r3 = p3.add_run("Local AI Agent  |  RAG Pipeline  |  Guardrails  |  Native Tool Calling")
r3.font.size = Pt(10); rc(r3, GOLD)

divider(doc)

# ==============================================================
# SECTION 1 — OVERVIEW
# ==============================================================
heading1(doc, "SECTION 1 — PROJECT OVERVIEW")
body(doc,
     "my-first-agent is a fully local AI agent built with Python and Ollama. "
     "It runs 100% offline on your machine using the llama3.2 model. "
     "The project is split into three connected modules:", WHITE)

for f in [
    "agent.py     — Main agent loop. Imports and uses rag.py as a module.",
    "rag.py       — RAG module. Handles PDF ingestion, embeddings, and search.",
    "guardrails.py — Safety layer. PII redaction and prompt injection defense.",
]:
    bullet(doc, f, GREEN)

note_box(doc,
    "agent.py imports from rag.py. rag.py is a standalone module "
    "that can also be run independently (python rag.py).")

divider(doc)

# ==============================================================
# SECTION 2 — FILE STRUCTURE
# ==============================================================
heading1(doc, "SECTION 2 — PROJECT FILE STRUCTURE")
code(doc, [
    "D:\\my-first-agent\\",
    "|",
    "+-- agent.py            <- Main AI agent (entry point)",
    "|     imports: rag.py, guardrails.py",
    "|",
    "+-- rag.py              <- RAG module (imported by agent.py)",
    "|     Provides: build_knowledge_base(), search_pdfs()",
    "|     Can also run standalone: python rag.py",
    "|",
    "+-- guardrails.py       <- Input & Output safety layer",
    "|     Provides: validate_input(), validate_output(), redact_pii()",
    "|",
    "+-- test_guardrails.py  <- Unit tests for guardrails",
    "+-- memory.json         <- Persistent conversation history (auto-created)",
    "+-- generate_doc.py     <- Script that generated this document",
    "+-- documents/          <- Drop your PDF files here for RAG",
    "+-- .venv/              <- Python virtual environment",
])

divider(doc)

# ==============================================================
# SECTION 3 — MODULE CONNECTION DIAGRAM
# ==============================================================
heading1(doc, "SECTION 3 — HOW THE MODULES ARE CONNECTED")
body(doc, "Import relationships between the three files:", WHITE)
code(doc, [
    "",
    "  agent.py",
    "  |",
    "  +-- from rag import build_knowledge_base    <- index PDFs at startup",
    "  |   from rag import search_pdfs             <- expose as LLM tool",
    "  |",
    "  +-- from guardrails import validate_input   <- check user input",
    "      from guardrails import validate_output  <- check LLM output",
    "",
    "  rag.py  (no imports from agent.py - no circular dependency)",
    "  |",
    "  +-- from ollama import chat                 <- generate answers",
    "  +-- from sentence_transformers import ...   <- create embeddings",
    "  +-- from pypdf import PdfReader             <- read PDFs",
    "",
    "  guardrails.py",
    "  |",
    "  +-- import re                               <- pattern matching only",
    "",
])

note_box(doc,
    "Previously rag.py imported from agent.py (circular risk). "
    "Now the dependency flows one way: agent.py -> rag.py -> external libs.")

divider(doc)

# ==============================================================
# SECTION 4 — PREREQUISITES
# ==============================================================
heading1(doc, "SECTION 4 — PREREQUISITES")
heading2(doc, "4.1  Install Python 3.10+")
body(doc, "Download from: https://www.python.org/downloads/")
body(doc, "Check 'Add Python to PATH' during installation.")
heading2(doc, "4.2  Install Ollama")
body(doc, "Download from: https://ollama.com")
heading2(doc, "4.3  Pull llama3.2 model")
code(doc, ["ollama pull llama3.2"])

divider(doc)

# ==============================================================
# SECTION 5 — STEP-BY-STEP SETUP
# ==============================================================
heading1(doc, "SECTION 5 — STEP-BY-STEP SETUP")

step_heading(doc, 1, "Create the project folder")
code(doc, ["mkdir D:\\my-first-agent", "cd D:\\my-first-agent"])

step_heading(doc, 2, "Create and activate a Virtual Environment")
code(doc, [
    "python -m venv .venv",
    "",
    "# Activate on Windows:",
    ".venv\\Scripts\\activate",
])
body(doc, "Your terminal will show (.venv) when the environment is active.")

step_heading(doc, 3, "Install all required packages")
code(doc, [
    "pip install ollama",
    "pip install pypdf",
    "pip install sentence-transformers",
    "pip install numpy",
    "pip install python-docx   # only needed to regenerate this document",
])
body(doc, "Package roles:")
for pkg in [
    "ollama               -> Python client to talk to local Ollama LLMs",
    "pypdf                -> Extract text from PDF files",
    "sentence-transformers -> Create semantic vector embeddings for RAG",
    "numpy                -> Fast vector math for cosine similarity search",
]:
    bullet(doc, pkg)

step_heading(doc, 4, "Create the documents folder")
code(doc, [
    "mkdir D:\\my-first-agent\\documents",
    "# Drop any PDF files here to make them searchable by the agent",
])

step_heading(doc, 5, "Create the three source files")
body(doc, "Create agent.py, rag.py, and guardrails.py — see Sections 6, 7, 8.")

divider(doc)

# ==============================================================
# SECTION 6 — agent.py
# ==============================================================
heading1(doc, "SECTION 6 — agent.py  (Main Agent)")

heading2(doc, "What it does")
for line in [
    "Imports build_knowledge_base and search_pdfs from rag.py",
    "Imports validate_input and validate_output from guardrails.py",
    "At startup: builds the PDF vector index via rag.py",
    "Accepts user input and runs it through guardrails",
    "Sends messages to Ollama llama3.2 with a tools schema",
    "LLM autonomously decides: use calculator, search PDFs, or answer directly",
    "Tool results are fed back into conversation for final answer",
    "Saves conversation to memory.json after each turn",
]:
    bullet(doc, line)

heading2(doc, "Full Source Code")
code(doc, [
    'from ollama import chat',
    'import json, os, ast, operator',
    '',
    '# Project modules',
    'from guardrails import validate_input, validate_output',
    'from rag import build_knowledge_base, search_pdfs',
    '',
    'MODEL       = "llama3.2"',
    'MEMORY_FILE = "memory.json"',
    '',
    '',
    '# ── Tool 1: Calculator ──────────────────────────────────────',
    'def calculator(expression: str) -> str:',
    '    allowed_operators = {',
    '        ast.Add:  operator.add,   ast.Sub:  operator.sub,',
    '        ast.Mult: operator.mul,   ast.Div:  operator.truediv,',
    '        ast.Pow:  operator.pow,   ast.Mod:  operator.mod,',
    '        ast.USub: operator.neg,',
    '    }',
    '    def evaluate(node):',
    '        if isinstance(node, ast.Constant):',
    '            if isinstance(node.value, (int, float)): return node.value',
    '            raise ValueError("Invalid number")',
    '        if isinstance(node, ast.BinOp):',
    '            op = allowed_operators.get(type(node.op))',
    '            if op is None: raise ValueError("Operation not allowed")',
    '            return op(evaluate(node.left), evaluate(node.right))',
    '        if isinstance(node, ast.UnaryOp):',
    '            op = allowed_operators.get(type(node.op))',
    '            if op is None: raise ValueError("Operation not allowed")',
    '            return op(evaluate(node.operand))',
    '        raise ValueError("Invalid expression")',
    '    try:',
    '        return str(evaluate(ast.parse(expression, mode="eval").body))',
    '    except Exception as e:',
    '        return f"Could not calculate: {e}"',
    '',
    '',
    '# ── Tool 2: PDF Search (imported from rag.py) ───────────────',
    'def pdf_search_tool(query: str) -> str:',
    '    return search_pdfs(query, llm_model=MODEL)',
    '',
    '',
    '# ── Tool Registry ───────────────────────────────────────────',
    'TOOLS = [',
    '    {',
    '        "type": "function",',
    '        "function": {',
    '            "name": "calculator",',
    '            "description": "Evaluates a math expression. Use for any arithmetic.",',
    '            "parameters": {',
    '                "type": "object",',
    '                "properties": {',
    '                    "expression": {"type": "string",',
    '                        "description": "Math expression e.g. 25 * 8"}',
    '                },',
    '                "required": ["expression"],',
    '            },',
    '        },',
    '    },',
    '    {',
    '        "type": "function",',
    '        "function": {',
    '            "name": "pdf_search_tool",',
    '            "description": "Searches PDF documents and returns a grounded answer.",',
    '            "parameters": {',
    '                "type": "object",',
    '                "properties": {',
    '                    "query": {"type": "string",',
    '                        "description": "Question to look up in PDF documents"}',
    '                },',
    '                "required": ["query"],',
    '            },',
    '        },',
    '    },',
    ']',
    '',
    'TOOL_MAP = {',
    '    "calculator":      calculator,',
    '    "pdf_search_tool": pdf_search_tool,',
    '}',
    '',
    '',
    '# ── Memory ──────────────────────────────────────────────────',
    'def load_memory():',
    '    if not os.path.exists(MEMORY_FILE): return []',
    '    try:',
    '        with open(MEMORY_FILE, "r", encoding="utf-8") as f:',
    '            return json.load(f)',
    '    except json.JSONDecodeError:',
    '        return []',
    '',
    'def save_memory(messages):',
    '    with open(MEMORY_FILE, "w", encoding="utf-8") as f:',
    '        json.dump(messages, f, indent=2, ensure_ascii=False)',
    '',
    '',
    '# ── System Prompt ───────────────────────────────────────────',
    'SYSTEM_PROMPT = """',
    'You are a helpful local AI assistant with two tools:',
    '1. calculator      - Use for any math or arithmetic.',
    '2. pdf_search_tool - Use to find information in PDF documents.',
    'Do not invent facts.',
    '"""',
    '',
    '',
    '# ── Startup ─────────────────────────────────────────────────',
    'print("================================")',
    'print("        LOCAL AI AGENT")',
    'print("================================")',
    'build_knowledge_base()   # <-- calls rag.py at startup',
    'conversation = load_memory()',
    'messages = [{"role": "system", "content": SYSTEM_PROMPT}]',
    'messages.extend(conversation)',
    '',
    '',
    '# ── Main Loop ───────────────────────────────────────────────',
    'while True:',
    '    user_input = input("You: ").strip()',
    '    if not user_input: continue',
    '',
    '    if user_input.lower() == "exit":',
    '        print("Goodbye!"); break',
    '',
    '    if user_input.lower() == "clear":',
    '        messages = [{"role": "system", "content": SYSTEM_PROMPT}]',
    '        save_memory([]); print("Memory cleared.\\n"); continue',
    '',
    '    if user_input.lower() == "reload":',
    '        build_knowledge_base(); continue   # re-index PDFs',
    '',
    '    # Guardrail: validate & sanitize input',
    '    is_safe, user_input, reason = validate_input(user_input)',
    '    if not is_safe:',
    '        print(f"\\n[Guardrail Blocked]: {reason}\\n"); continue',
    '',
    '    messages.append({"role": "user", "content": user_input})',
    '',
    '    # Agentic loop: model calls tools until it has a final answer',
    '    while True:',
    '        response          = chat(model=MODEL, messages=messages, tools=TOOLS)',
    '        assistant_message = response.message',
    '        messages.append(assistant_message)',
    '',
    '        if not assistant_message.tool_calls: break',
    '',
    '        for tc in assistant_message.tool_calls:',
    '            name   = tc.function.name',
    '            args   = tc.function.arguments',
    '            print(f"  [Agent -> {name}] Args: {args}")',
    '            result = TOOL_MAP[name](**args) if name in TOOL_MAP else f"Unknown: {name}"',
    '            print(f"  [Result: {str(result)[:120]}]")',
    '            messages.append({"role": "tool", "content": str(result)})',
    '',
    '    raw_answer   = assistant_message.content or ""',
    '    _, answer, _ = validate_output(raw_answer)  # output guardrail',
    '    save_memory(messages[1:])',
    '    print(f"\\nAgent: {answer}\\n")',
])

divider(doc)

# ==============================================================
# SECTION 7 — rag.py
# ==============================================================
heading1(doc, "SECTION 7 — rag.py  (RAG Module)")

heading2(doc, "What it does")
for line in [
    "Importable module — used by agent.py as a library",
    "Also runnable standalone: python rag.py",
    "Loads all PDFs from the documents/ folder using pypdf",
    "Splits text into 500-word chunks for granular retrieval",
    "Creates semantic embeddings using all-MiniLM-L6-v2",
    "Finds top-3 most relevant chunks via cosine similarity (numpy)",
    "Generates a grounded answer using Ollama llama3.2",
    "Returns answer with source file and page number citations",
]:
    bullet(doc, line)

heading2(doc, "Full Source Code")
code(doc, [
    'import os, numpy as np',
    'from pypdf import PdfReader',
    'from sentence_transformers import SentenceTransformer',
    'from ollama import chat',
    '',
    'DOCUMENTS_FOLDER = "documents"',
    'EMBEDDING_MODEL  = "all-MiniLM-L6-v2"',
    'DEFAULT_MODEL    = "llama3.2"',
    '',
    '# Module-level state (shared when imported by agent.py)',
    '_embedding_model = None',
    '_chunks          = []',
    '_embeddings      = None',
    '',
    '',
    'def get_embedding_model():',
    '    global _embedding_model',
    '    if _embedding_model is None:',
    '        print(f"[RAG] Loading embedding model...")',
    '        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)',
    '    return _embedding_model',
    '',
    '',
    'def load_pdfs():',
    '    documents = []',
    '    if not os.path.exists(DOCUMENTS_FOLDER):',
    '        os.makedirs(DOCUMENTS_FOLDER)',
    '        return documents',
    '    for filename in os.listdir(DOCUMENTS_FOLDER):',
    '        if filename.lower().endswith(".pdf"):',
    '            path   = os.path.join(DOCUMENTS_FOLDER, filename)',
    '            reader = PdfReader(path)',
    '            for num, page in enumerate(reader.pages):',
    '                text = page.extract_text()',
    '                if text:',
    '                    documents.append({"file": filename, "page": num+1, "text": text})',
    '    return documents',
    '',
    '',
    'def split_text(text, chunk_size=500):',
    '    words = text.split()',
    '    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]',
    '',
    '',
    'def build_knowledge_base():',
    '    """Loads all PDFs and creates vector index. Called by agent.py at startup."""',
    '    global _chunks, _embeddings',
    '    pages = load_pdfs()',
    '    if not pages:',
    '        print("[RAG] No PDFs found in documents/")',
    '        _chunks = []; _embeddings = None; return 0, 0',
    '    raw_chunks = []',
    '    for page in pages:',
    '        for chunk in split_text(page["text"]):',
    '            raw_chunks.append({"file": page["file"], "page": page["page"], "text": chunk})',
    '    model      = get_embedding_model()',
    '    texts      = [c["text"] for c in raw_chunks]',
    '    _embeddings = model.encode(texts, normalize_embeddings=True)',
    '    _chunks     = raw_chunks',
    '    print(f"[RAG] Indexed {len(_chunks)} chunks from {len(pages)} page(s).")',
    '    return len(_chunks), len(pages)',
    '',
    '',
    'def is_knowledge_base_ready():',
    '    return len(_chunks) > 0 and _embeddings is not None',
    '',
    '',
    'def search(query, top_k=3):',
    '    """Returns top_k most relevant chunks for query."""',
    '    if not is_knowledge_base_ready(): return []',
    '    model     = get_embedding_model()',
    '    q_emb     = model.encode([query], normalize_embeddings=True)[0]',
    '    scores    = np.dot(_embeddings, q_emb)',
    '    best_idx  = np.argsort(scores)[::-1][:min(top_k, len(_chunks))]',
    '    return [{"score": float(scores[i]), "file": _chunks[i]["file"],',
    '             "page": _chunks[i]["page"],  "text": _chunks[i]["text"]}',
    '            for i in best_idx]',
    '',
    '',
    'def generate_answer(query, results, llm_model=DEFAULT_MODEL):',
    '    """Generates a grounded LLM answer from retrieved chunks."""',
    '    if not results: return "I could not find enough information in the PDFs."',
    '    context  = "\\n\\n".join([',
    '        f"Source: {r[\'file\']}, Page: {r[\'page\']}\\n{r[\'text\']}"',
    '        for r in results',
    '    ])',
    '    response = chat(model=llm_model, messages=[',
    '        {"role": "system", "content":',
    '            "You are a PDF Q&A assistant. Answer ONLY from the PDF context. "',
    '            "If not enough info say: I could not find enough information in the PDFs. "',
    '            "Always cite source file and page."},',
    '        {"role": "user", "content":',
    '            f"Question: {query}\\n\\nPDF Context:\\n{context}\\n\\nAnswer:"}',
    '    ])',
    '    return response.message.content or "I could not generate an answer."',
    '',
    '',
    'def search_pdfs(query: str, llm_model=DEFAULT_MODEL) -> str:',
    '    """Full RAG pipeline. This function is imported and used as a tool in agent.py."""',
    '    if not is_knowledge_base_ready():',
    '        return "No PDFs loaded. Add PDFs to documents/ and type reload."',
    '    results = search(query)',
    '    answer  = generate_answer(query, results, llm_model)',
    '    sources = " | ".join(f"{r[\'file\']} p.{r[\'page\']}" for r in results)',
    '    return f"{answer}\\n\\n[Sources: {sources}]"',
    '',
    '',
    '# ── Standalone mode ─────────────────────────────────────────',
    'if __name__ == "__main__":',
    '    num_chunks, num_pages = build_knowledge_base()',
    '    if num_chunks == 0:',
    '        print("No PDFs found. Add PDFs to documents/ and try again.")',
    '    else:',
    '        print(f"Ready. Indexed {num_chunks} chunks from {num_pages} pages.")',
    '        print("Type exit to quit.")',
    '        while True:',
    '            query = input("\\nAsk about your PDFs: ").strip()',
    '            if not query: continue',
    '            if query.lower() == "exit": break',
    '            results = search(query)',
    '            print("\\nANSWER:")',
    '            print(generate_answer(query, results))',
    '            print("\\nSOURCES:")',
    '            for r in results:',
    '                print(f"  - {r[\'file\']} (page {r[\'page\']})")',
])

divider(doc)

# ==============================================================
# SECTION 8 — guardrails.py
# ==============================================================
heading1(doc, "SECTION 8 — guardrails.py  (Safety Layer)")

heading2(doc, "What it does")
for line in [
    "Detects and redacts PII: emails, phone numbers, SSNs, credit cards",
    "Blocks prompt injection attacks before they reach the LLM",
    "Enforces maximum input length (4000 characters)",
    "Scrubs any PII that might appear in the model output",
]:
    bullet(doc, line)

heading2(doc, "Full Source Code")
code(doc, [
    'import re',
    '',
    'PII_PATTERNS = {',
    '    "EMAIL"       : r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",',
    '    "PHONE"       : r"\\b(?:\\+?\\d{1,3}[-.\\s]?)?\\(?\\d{3}\\)?[-.\\s]?\\d{3}[-.\\s]?\\d{4}\\b",',
    '    "SSN"         : r"\\b\\d{3}-\\d{2}-\\d{4}\\b",',
    '    "CREDIT_CARD" : r"\\b(?:\\d[ -]*?){13,16}\\b",',
    '}',
    '',
    'PROMPT_INJECTION_PATTERNS = [',
    '    r"ignore\\s+(all\\s+)?(previous|above)\\s+instructions",',
    '    r"system\\s*:\\s*override",',
    '    r"disregard\\s+(the\\s+)?system\\s+prompt",',
    '    r"you\\s+are\\s+now\\s+a\\s+unrestricted",',
    '    r"jailbreak",',
    '    r"DAN\\s+mode",',
    '    r"forget\\s+(all\\s+)?your\\s+rules",',
    ']',
    '',
    'MAX_INPUT_LENGTH = 4000',
    '',
    '',
    'def redact_pii(text: str) -> str:',
    '    sanitized = text',
    '    for pii_type, pattern in PII_PATTERNS.items():',
    '        sanitized = re.sub(pattern, f"[{pii_type}_REDACTED]", sanitized)',
    '    return sanitized',
    '',
    '',
    'def validate_input(user_input: str):',
    '    if not user_input or not user_input.strip():',
    '        return False, "", "Empty input provided."',
    '    if len(user_input) > MAX_INPUT_LENGTH:',
    '        return False, "", f"Input exceeds {MAX_INPUT_LENGTH} characters."',
    '    for pattern in PROMPT_INJECTION_PATTERNS:',
    '        if re.search(pattern, user_input, re.IGNORECASE):',
    '            return False, "", "Input blocked: Potential prompt injection detected."',
    '    return True, redact_pii(user_input), ""',
    '',
    '',
    'def validate_output(output_text: str):',
    '    if not output_text: return True, "", ""',
    '    return True, redact_pii(output_text), ""',
])

divider(doc)

# ==============================================================
# SECTION 9 — HOW TO RUN
# ==============================================================
heading1(doc, "SECTION 9 — HOW TO RUN")

step_heading(doc, 1, "Start Ollama")
code(doc, ["ollama serve", "# Keep this terminal open"])

step_heading(doc, 2, "Activate virtual environment")
code(doc, ["cd D:\\my-first-agent", ".venv\\Scripts\\activate"])

step_heading(doc, 3, "Run the main agent (recommended)")
code(doc, ["python agent.py"])
body(doc, "This starts the full agent with calculator + PDF search + memory + guardrails.")
code(doc, [
    "================================",
    "        LOCAL AI AGENT",
    "================================",
    "[RAG] Indexed 42 chunks from 5 page(s) across 2 PDF(s).",
    "",
    "Tools     : calculator | pdf_search_tool (via rag.py)",
    "Memory    : ACTIVE",
    "Guardrails: ACTIVE (PII + Prompt Injection)",
    "",
    "Commands:",
    "  exit   -> Quit the agent",
    "  clear  -> Erase conversation memory",
    "  reload -> Re-index PDFs from documents/",
    "================================",
    "",
    "You: _",
])

step_heading(doc, 4, "Run rag.py standalone (optional)")
body(doc, "First drop PDF files into the documents/ folder, then:")
code(doc, ["python rag.py"])

step_heading(doc, 5, "Run guardrail unit tests")
code(doc, [
    "python test_guardrails.py",
    "# Expected: Ran 3 tests in 0.003s  OK",
])

divider(doc)

# ==============================================================
# SECTION 10 — COMPONENTS TABLE
# ==============================================================
heading1(doc, "SECTION 10 — ALL COMPONENTS AT A GLANCE")

rows = [
    ("Component",             "File",               "Technology",                   "Status"),
    ("LLM Engine",            "agent.py",           "Ollama llama3.2",              "Active"),
    ("Native Tool Calling",   "agent.py",           "Ollama tools schema",          "Active"),
    ("Calculator Tool",       "agent.py",           "Python ast module",            "Active"),
    ("PDF Search Tool",       "agent.py",           "Imports search_pdfs (rag.py)", "Active"),
    ("Persistent Memory",     "agent.py",           "JSON (memory.json)",           "Active"),
    ("Input Guardrails",      "guardrails.py",      "Regex pattern matching",       "Active"),
    ("Output Guardrails",     "guardrails.py",      "PII regex scrubbing",          "Active"),
    ("PDF Loader",            "rag.py",             "pypdf (PdfReader)",            "Active"),
    ("Text Chunker",          "rag.py",             "Word-based sliding window",    "Active"),
    ("Embedding Model",       "rag.py",             "all-MiniLM-L6-v2",           "Active"),
    ("Vector Search",         "rag.py",             "numpy dot product",            "Active"),
    ("Grounded Answer Gen",   "rag.py",             "Ollama llama3.2",              "Active"),
    ("Unit Tests",            "test_guardrails.py", "Python unittest",              "Active"),
]

table = doc.add_table(rows=len(rows), cols=4)
table.style = 'Table Grid'
for ri, row_data in enumerate(rows):
    cells = table.rows[ri].cells
    for ci, text in enumerate(row_data):
        p = cells[ci].paragraphs[0]
        r = p.add_run(text)
        r.font.size = Pt(9); r.font.name = "Calibri"
        if ri == 0:
            r.bold = True; rc(r, WHITE)
            cell_shd(cells[ci], '1E3A5F')
        else:
            rc(r, RGBColor(0x22, 0x22, 0x22))

divider(doc)

# ==============================================================
# SECTION 11 — UPGRADE ROADMAP
# ==============================================================
heading1(doc, "SECTION 11 — UPGRADE ROADMAP")

roadmap = [
    ("DONE",        "Conversational AI with llama3.2"),
    ("DONE",        "Persistent Memory (memory.json)"),
    ("DONE",        "Safe Calculator Tool (AST eval)"),
    ("DONE",        "RAG — PDF Q&A Pipeline (rag.py)"),
    ("DONE",        "Guardrails — PII Redaction"),
    ("DONE",        "Guardrails — Prompt Injection Defense"),
    ("DONE",        "Native Ollama Tool Calling"),
    ("DONE",        "agent.py imports rag.py (proper module connection)"),
    ("NEXT",        "Multi-Step ReAct Reasoning Loop"),
    ("NEXT",        "Web Search Tool (DuckDuckGo API)"),
    ("SECURITY",    "Rate Limiting"),
    ("SECURITY",    "RAG Hallucination / Groundedness Check"),
    ("SECURITY",    "Memory Auto-Summarization"),
    ("POLISH",      "Streaming Responses (token-by-token output)"),
    ("POLISH",      "Logging System (.log file)"),
    ("POLISH",      "Chat History Viewer command"),
    ("POLISH",      "Multi-modal Vision (llava model)"),
]

for status, desc in roadmap:
    p = doc.add_paragraph()
    shd(p, '1E1E2E')
    p.paragraph_format.left_indent  = Inches(0.2)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    r1 = p.add_run(f"  [{status}]  ")
    r1.bold = True; r1.font.size = Pt(10)
    if status == "DONE":
        rc(r1, GREEN)
    elif status == "NEXT":
        rc(r1, GOLD)
    elif status == "SECURITY":
        rc(r1, RED_SOFT)
    else:
        rc(r1, MUTED)
    r2 = p.add_run(f" {desc}")
    r2.font.size = Pt(10)
    rc(r2, WHITE if status == "DONE" else MUTED)

divider(doc)

# Footer
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
shd(p, '1E1E2E')
p.paragraph_format.space_before = Pt(10)
r = p.add_run("my-first-agent  |  Built with Python & Ollama  |  Runs 100% Locally")
r.italic = True; r.font.size = Pt(9); rc(r, MUTED)

# ── Save ──────────────────────────────────────────────────────
OUT = r"D:\my-first-agent\my-first-agent-guide.docx"
doc.save(OUT)
print(f"Saved: {OUT}")
