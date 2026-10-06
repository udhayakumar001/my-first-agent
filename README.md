# Local AI Agent

A command-line AI assistant built with Python and Ollama. It can answer general questions, use a restricted calculator for arithmetic, and search local PDFs with retrieval-augmented generation (RAG). Conversation history is persisted in `memory.json`.

## Features

- **Local chat and tool calling:** Uses Ollama's `llama3.2` model.
- **PDF search:** Extracts PDF text, embeds it with Hugging Face's `all-MiniLM-L6-v2`, retrieves relevant passages, and generates grounded answers with file and page citations.
- **Safe calculator:** Evaluates arithmetic through an allowlist of Python AST operations instead of `eval`.
- **Guardrails:** Blocks several known prompt-injection patterns, limits input length, and redacts detected PII in inputs and answers.
- **Persistent memory:** Saves conversation messages to `memory.json`; type `clear` to erase them.

## Technology stack

- **Python** for the agent, RAG pipeline, guardrails, and tests
- **Ollama + Llama 3.2 (3B SLM)** for local chat and tool calling
- **Hugging Face Sentence Transformers**, using `all-MiniLM-L6-v2`, for text embeddings
- **pypdf** for PDF text extraction and **NumPy** for similarity search
- **Python AST and `unittest`** for restricted arithmetic evaluation and guardrail tests
- **python-docx** in `generate_doc.py` for creating the project guide

## Resume project summary

**Local AI Agent with PDF RAG** — Built a Python-based local AI assistant using Ollama's Llama 3.2 (3B) SLM with native tool calling. Implemented PDF question answering with a Hugging Face `all-MiniLM-L6-v2` embedding model, NumPy-based semantic retrieval, and cited responses; added AST-restricted calculator execution, PII/prompt-injection guardrails, and persistent JSON conversation memory.

## Prerequisites

- Python 3.10 or newer
- [Ollama](https://ollama.com/download) installed locally
- The `llama3.2` model available in Ollama
- Internet access on first use to download the `all-MiniLM-L6-v2` embedding model, unless it is already cached

## Setup

From the project root, create and activate a virtual environment, then install the runtime packages:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install ollama numpy pypdf sentence-transformers
```

On macOS or Linux, activate the environment with `source .venv/bin/activate` instead. There is no `requirements.txt` in this project.

Ensure Ollama is running and download the chat model:

```powershell
ollama pull llama3.2
```

Place PDF files in `documents/`. The included `AI-Notes.pdf` is indexed automatically at startup. Once dependencies are installed and Ollama is available, run:

```powershell
python agent.py
```

## Usage

Enter a request at the `You:` prompt. For example:

```text
What is 25 * 4?
Summarize the main ideas in AI-Notes.pdf.
```

The agent selects the calculator for arithmetic and searches the PDFs for document questions. Available commands:

- `reload` — re-index PDFs after adding or changing files in `documents/`
- `clear` — erase saved conversation history
- `exit` — quit

Run the guardrail tests with `python -m unittest test_guardrails.py`.

## Project structure

```text
.
├── agent.py                  # Ollama chat loop, tools, and conversation memory
├── rag.py                    # PDF loading, embeddings, retrieval, and grounded answers
├── guardrails.py             # Input checks and PII redaction
├── test_guardrails.py        # Guardrail unit tests
├── memory.json               # Persisted conversation history
├── documents/
│   └── AI-Notes.pdf          # Example PDF indexed by the RAG pipeline
├── generate_doc.py           # Guide document generator
└── my-first-agent-guide.docx # Generated project guide
```

## Running Ollama locally

Ollama must be available on the same machine while the agent runs. The Ollama desktop app usually starts the service automatically; otherwise, run `ollama serve` in a separate terminal. The agent connects to Ollama locally using its default connection and requires no cloud API key. Check installed models with `ollama list`.

PDF text is embedded and indexed in memory at startup; the project does not upload PDFs to a hosted vector database. The embedding model is downloaded on first use if it is not cached locally.
