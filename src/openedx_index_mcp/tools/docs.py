"""Documentation tools: search_docs, list_docs, get_doc."""

import os
from typing import Any, Optional

from code_index_mcp.services.search_service import SearchService

from ..services.bootstrap import get_ctx
from ..services.docs_index import get_docs_index
from .. import settings


def search_docs(
    query: str,
    doc_type: str = "all",
    max_results: int = 10,
) -> dict[str, Any]:
    """
    Full-text search across all Open edX documentation (RST and MD files).

    Args:
        query: Search text or regex pattern
        doc_type: Filter by type: 'adr', 'how-to', 'reference', 'readme',
                  'changelog', 'guide', or 'all' (default)
        max_results: Maximum results to return

    Returns:
        Dict with 'results' list and 'pagination' info
    """
    ctx = get_ctx()

    # Search RST files
    rst_results = SearchService(ctx).search_code(
        pattern=query,
        case_sensitive=False,
        context_lines=2,
        file_pattern="*.rst",
        max_results=max_results,
    )

    # Search MD files
    md_results = SearchService(ctx).search_code(
        pattern=query,
        case_sensitive=False,
        context_lines=2,
        file_pattern="*.md",
        max_results=max_results,
    )

    # Merge results
    all_results = rst_results.get("results", []) + md_results.get("results", [])

    # Filter by doc_type if specified
    if doc_type != "all":
        docs_index = get_docs_index()
        doc_paths = {d["path"] for d in docs_index if d["doc_type"] == doc_type}
        all_results = [
            r for r in all_results
            if r.get("file", "").lstrip("./") in doc_paths
        ]

    # Trim to max_results
    all_results = all_results[:max_results]

    return {
        "results": all_results,
        "total": len(all_results),
        "doc_type_filter": doc_type,
    }


def list_docs(
    doc_type: Optional[str] = None,
    repo: Optional[str] = None,
) -> list[dict[str, str]]:
    """
    List available documentation with titles.

    Args:
        doc_type: Filter by type: 'adr', 'how-to', 'reference', 'readme',
                  'changelog', 'guide'. None for all.
        repo: Filter by repo (e.g., 'core-libraries/openedx-events'). None for all.

    Returns:
        List of {"path", "title", "doc_type", "repo"} dicts
    """
    docs = get_docs_index()

    if doc_type:
        docs = [d for d in docs if d["doc_type"] == doc_type]

    if repo:
        docs = [d for d in docs if d["repo"] == repo]

    return docs


def get_doc(path: str) -> str:
    """
    Read full content of a documentation file.

    Args:
        path: Path relative to sources root (must be .rst or .md)

    Returns:
        File content as string
    """
    ext = os.path.splitext(path)[1].lower()
    if ext not in (".rst", ".md"):
        raise ValueError(f"Not a documentation file (must be .rst or .md): {path}")

    sources_dir = os.path.abspath(settings.SOURCES_DIR)
    full_path = os.path.normpath(os.path.join(sources_dir, path))

    # Security: prevent path traversal
    if not full_path.startswith(sources_dir):
        raise ValueError(f"Path traversal not allowed: {path}")

    if not os.path.isfile(full_path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(full_path, encoding="utf-8", errors="replace") as f:
        return f.read()
