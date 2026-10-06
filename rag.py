"""
rag.py — RAG (Retrieval-Augmented Generation) Module

Provides PDF ingestion, text chunking, vector embedding,
semantic search, and grounded answer generation.

Can be:
  - Imported by agent.py as a module
  - Run standalone: python rag.py
"""

import os
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from ollama import chat

DOCUMENTS_FOLDER = "documents"
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"
DEFAULT_MODEL    = "llama3.2"

# ============================================================
# INTERNAL STATE (module-level, shared when imported)
# ============================================================

_embedding_model = None
_chunks          = []
_embeddings      = None


# ============================================================
# EMBEDDING MODEL (lazy-loaded)
# ============================================================

def get_embedding_model():
    """Loads the embedding model once and reuses it."""
    global _embedding_model
    if _embedding_model is None:
        print(f"[RAG] Loading embedding model ({EMBEDDING_MODEL})...")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        print("[RAG] Embedding model ready.")
    return _embedding_model


# ============================================================
# PDF LOADING & CHUNKING
# ============================================================

def load_pdfs():
    """Reads all PDFs from the documents/ folder page by page."""
    documents = []
    if not os.path.exists(DOCUMENTS_FOLDER):
        os.makedirs(DOCUMENTS_FOLDER)
        return documents

    for filename in os.listdir(DOCUMENTS_FOLDER):
        if filename.lower().endswith(".pdf"):
            path   = os.path.join(DOCUMENTS_FOLDER, filename)
            reader = PdfReader(path)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    documents.append({
                        "file": filename,
                        "page": page_num + 1,
                        "text": text,
                    })
    return documents


def split_text(text, chunk_size=500):
    """Splits text into overlapping word chunks."""
    words  = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks


# ============================================================
# KNOWLEDGE BASE
# ============================================================

def build_knowledge_base():
    """
    Loads all PDFs and builds the in-memory vector index.
    Call this once at startup, or after adding new PDFs.
    Returns: (num_chunks, num_pages)
    """
    global _chunks, _embeddings

    pages = load_pdfs()

    if not pages:
        print("[RAG] No PDFs found in documents/ — PDF search unavailable.")
        _chunks     = []
        _embeddings = None
        return 0, 0

    raw_chunks = []
    for page in pages:
        for chunk in split_text(page["text"]):
            raw_chunks.append({
                "file": page["file"],
                "page": page["page"],
                "text": chunk,
            })

    model      = get_embedding_model()
    texts      = [c["text"] for c in raw_chunks]
    embeddings = model.encode(texts, normalize_embeddings=True)

    _chunks     = raw_chunks
    _embeddings = embeddings

    num_pdfs = len(set(c["file"] for c in raw_chunks))
    print(f"[RAG] Indexed {len(_chunks)} chunks from {len(pages)} page(s) across {num_pdfs} PDF(s).")
    return len(_chunks), len(pages)


def is_knowledge_base_ready():
    """Returns True if PDFs have been indexed."""
    return len(_chunks) > 0 and _embeddings is not None


# ============================================================
# SEARCH
# ============================================================

def search(query, top_k=3):
    """
    Finds the top_k most relevant chunks for the query.
    Returns a list of result dicts with score, file, page, text.
    """
    if not is_knowledge_base_ready():
        return []

    model     = get_embedding_model()
    query_emb = model.encode([query], normalize_embeddings=True)[0]
    scores    = np.dot(_embeddings, query_emb) # type: ignore
    top_k     = min(top_k, len(_chunks))
    best_idx  = np.argsort(scores)[::-1][:top_k]

    return [
        {
            "score": float(scores[i]),
            "file":  _chunks[i]["file"],
            "page":  _chunks[i]["page"],
            "text":  _chunks[i]["text"],
        }
        for i in best_idx
    ]


# ============================================================
# ANSWER GENERATION
# ============================================================

def generate_answer(query, results, llm_model=DEFAULT_MODEL):
    """
    Generates a grounded answer from retrieved PDF chunks using the LLM.
    Returns the answer string.
    """
    if not results:
        return "I couldn't find enough information in the PDFs."

    context = "\n\n".join([
        f"Source: {r['file']}, Page: {r['page']}\n{r['text']}"
        for r in results
    ])

    response = chat(
        model=llm_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a PDF question-answering assistant. "
                    "Answer ONLY using the provided PDF context. "
                    "If the context is insufficient, say: "
                    "'I couldn't find enough information in the PDFs.' "
                    "Always cite the source file and page when referencing information."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question: {query}\n\n"
                    f"PDF Context:\n{context}\n\n"
                    "Answer the question using only the context above."
                ),
            },
        ],
    )

    return response.message.content or "I couldn't generate an answer."


def search_pdfs(query: str, llm_model=DEFAULT_MODEL) -> str:
    """
    Full RAG pipeline: search → retrieve → generate answer.
    This is the function exposed as a tool in agent.py.
    Returns the answer with source references.
    """
    if not is_knowledge_base_ready():
        return (
            "No PDF documents are loaded. "
            "Please add PDF files to the documents/ folder and type 'reload'."
        )

    results = search(query)
    answer  = generate_answer(query, results, llm_model)
    sources = " | ".join(
        f"{r['file']} p.{r['page']}"
        for r in results
    )
    return f"{answer}\n\n[Sources: {sources}]"


# ============================================================
# STANDALONE MODE  (python rag.py)
# ============================================================

if __name__ == "__main__":

    num_chunks, num_pages = build_knowledge_base()

    if num_chunks == 0:
        print("No PDFs found. Add PDF files to the documents/ folder and try again.")
    else:
        print()
        print("================================")
        print("   PDF QUESTION-ANSWERING RAG")
        print("================================")
        print(f"Loaded {num_chunks} chunks from {num_pages} page(s).")
        print("Type 'exit' to quit.")
        print()

        while True:
            query = input("Ask about your PDFs: ").strip()

            if not query:
                continue

            if query.lower() == "exit":
                print("Goodbye!")
                break

            results = search(query)
            answer  = generate_answer(query, results)

            print()
            print("================================")
            print("ANSWER:")
            print("================================")
            print(answer)
            print()
            print("SOURCES:")
            for r in results:
                print(f"  - {r['file']} (page {r['page']})  [score: {r['score']:.3f}]")
            print()