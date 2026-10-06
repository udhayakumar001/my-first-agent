"""
agent.py — Main AI Agent

Features:
  - Conversational AI powered by Ollama (llama3.2)
  - Persistent conversation memory (memory.json)
  - Native Ollama tool calling
  - Tool 1: calculator  — safe AST-based math evaluation
  - Tool 2: search_pdfs — RAG pipeline (imported from rag.py)
  - Guardrails          — PII redaction & prompt injection defense
"""

from ollama import chat
import json
import os
import ast
import operator

# ── Project modules ───────────────────────────────────────────
from guardrails import validate_input, validate_output
from rag import build_knowledge_base, search_pdfs


MODEL       = "llama3.2"
MEMORY_FILE = "memory.json"


# ============================================================
# TOOL 1 — CALCULATOR
# ============================================================

def calculator(expression: str) -> str:
    """
    Safely evaluates a mathematical expression using Python AST.
    Supports: +, -, *, /, **, %
    """
    allowed_operators = {
        ast.Add:  operator.add,
        ast.Sub:  operator.sub,
        ast.Mult: operator.mul,
        ast.Div:  operator.truediv,
        ast.Pow:  operator.pow,
        ast.Mod:  operator.mod,
        ast.USub: operator.neg,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid number")
        if isinstance(node, ast.BinOp):
            left  = evaluate(node.left)
            right = evaluate(node.right)
            op    = allowed_operators.get(type(node.op))
            if op is None:
                raise ValueError("Operation not allowed")
            return op(left, right)
        if isinstance(node, ast.UnaryOp):
            operand = evaluate(node.operand)
            op      = allowed_operators.get(type(node.op))
            if op is None:
                raise ValueError("Operation not allowed")
            return op(operand)
        raise ValueError("Invalid expression")

    try:
        tree   = ast.parse(expression, mode="eval")
        result = evaluate(tree.body)
        return str(result)
    except Exception as e:
        return f"Could not calculate: {e}"


# ============================================================
# TOOL 2 — PDF SEARCH  (imported from rag.py)
# ============================================================
# search_pdfs(query: str) -> str
# Imported directly from rag.py — no duplication.
# rag.py manages: embedding model, PDF chunks, vector index.

def pdf_search_tool(query: str) -> str:
    """Wrapper that passes the agent's LLM model to the RAG pipeline."""
    return search_pdfs(query, llm_model=MODEL)


# ============================================================
# TOOL REGISTRY
# ============================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Evaluates a mathematical expression and returns the numeric result. "
                "Use for any arithmetic: +, -, *, /, powers (**), and modulo (%)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "A valid math expression string. "
                            "Examples: '25 * 8', '100 / 4', '2 ** 10', '17 % 3'"
                        ),
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "pdf_search_tool",
            "description": (
                "Searches the user's indexed PDF documents for relevant information "
                "and returns a grounded answer with source file and page references. "
                "Use this whenever the user asks about content in their documents or PDFs."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The question or topic to look up in the PDF documents.",
                    }
                },
                "required": ["query"],
            },
        },
    },
]

TOOL_MAP = {
    "calculator":     calculator,
    "pdf_search_tool": pdf_search_tool,
}


# ============================================================
# MEMORY
# ============================================================

def serialize_message(msg) -> dict:
    """
    Converts an Ollama Message object OR a plain dict into a
    JSON-serializable dict so it can be stored in memory.json.
    """
    if isinstance(msg, dict):
        return msg
    # Ollama Message object
    result = {
        "role":    getattr(msg, "role",    ""),
        "content": getattr(msg, "content", "") or "",
    }
    tool_calls = getattr(msg, "tool_calls", None)
    if tool_calls:
        result["tool_calls"] = [
            {
                "function": {
                    "name":      tc.function.name,
                    "arguments": tc.function.arguments,
                }
            }
            for tc in tool_calls
        ]
    return result


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_memory(messages):
    serializable = [serialize_message(m) for m in messages]
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a helpful local AI assistant with two tools:

1. calculator     — Use for any math or arithmetic calculation.
2. pdf_search_tool — Use to find information inside the user's PDF documents.

Rules:
- Always use calculator for arithmetic. Never calculate mentally.
- Use pdf_search_tool when the user asks about their documents.
- If neither tool applies, answer from your own knowledge.
- Do not invent facts.
"""


# ============================================================
# STARTUP
# ============================================================

print("================================")
print("        LOCAL AI AGENT")
print("================================")
print()
print("Initializing RAG module (rag.py)...")
build_knowledge_base()
print()
print("Tools     : calculator | pdf_search_tool (via rag.py)")
print("Memory    : ACTIVE")
print("Guardrails: ACTIVE (PII + Prompt Injection)")
print()
print("Commands:")
print("  exit   -> Quit the agent")
print("  clear  -> Erase conversation memory")
print("  reload -> Re-index PDFs from documents/")
print("================================")
print()

conversation = load_memory()
messages = [{"role": "system", "content": SYSTEM_PROMPT}]
messages.extend(conversation)


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    user_input = input("You: ").strip()

    if not user_input:
        continue

    # ── Special commands ─────────────────────────────────────
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if user_input.lower() == "clear":
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        save_memory([])
        print("Memory cleared.\n")
        continue

    if user_input.lower() == "reload":
        print("Reloading PDFs from documents/...")
        build_knowledge_base()
        print()
        continue

    # ── Input Guardrails ─────────────────────────────────────
    is_safe, user_input, reason = validate_input(user_input)
    if not is_safe:
        print(f"\n[Guardrail Blocked]: {reason}\n")
        continue

    # ── Add user message to conversation ─────────────────────
    messages.append({"role": "user", "content": user_input})

    # ── Agentic tool-use loop ────────────────────────────────
    # Model can call tools multiple times before final answer.
    final_content = ""

    while True:

        response          = chat(model=MODEL, messages=messages, tools=TOOLS)
        assistant_message = response.message

        # Convert Ollama Message object → plain dict immediately
        # so all messages in the list stay JSON-serializable
        assistant_dict = serialize_message(assistant_message)
        messages.append(assistant_dict)

        # Capture content for final answer
        final_content = assistant_dict.get("content", "") or ""

        # No tool calls → final answer reached
        if not assistant_message.tool_calls:
            break

        # Execute each requested tool call
        for tool_call in assistant_message.tool_calls:

            name = tool_call.function.name
            args = tool_call.function.arguments

            print(f"\n  [Agent -> {name}]")
            print(f"  [Args  : {args}]")

            if name in TOOL_MAP:
                result = TOOL_MAP[name](**args)
            else:
                result = f"Unknown tool: {name}"

            preview = str(result)[:150]
            print(f"  [Result: {preview}{'...' if len(str(result)) > 150 else ''}]\n")

            # Feed tool result back into conversation
            messages.append({"role": "tool", "content": str(result)})

    # ── Output Guardrails ────────────────────────────────────
    _, answer, _ = validate_output(final_content)

    # ── Persist conversation ─────────────────────────────────
    save_memory(messages[1:])

    print(f"\nAgent: {answer}\n")