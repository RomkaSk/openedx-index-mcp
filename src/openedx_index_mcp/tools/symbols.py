"""Symbol and file content tools."""

import os
from typing import Any

from code_index_mcp.services.code_intelligence_service import CodeIntelligenceService

from ..services.bootstrap import get_ctx
from .. import settings


def get_file_summary(file_path: str) -> dict[str, Any]:
    """
    Get symbols, imports, and metadata for a file.

    Args:
        file_path: Path relative to sources root (e.g., "common/openedx-platform/lms/urls.py")

    Returns:
        Dict with functions, classes, imports, line_count, etc.
    """
    ctx = get_ctx()
    return CodeIntelligenceService(ctx).analyze_file(file_path)


def get_symbol_body(file_path: str, symbol_name: str) -> dict[str, Any]:
    """
    Get the source code of a specific function, class, or method.

    Args:
        file_path: Path relative to sources root
        symbol_name: Symbol name (e.g., "MyClass.my_method")

    Returns:
        Dict with code, signature, docstring, line range, type
    """
    ctx = get_ctx()
    return CodeIntelligenceService(ctx).get_symbol_body(file_path, symbol_name)


def get_file_content(file_path: str) -> str:
    """
    Read a file from the indexed Open edX sources.

    Args:
        file_path: Path relative to sources root

    Returns:
        File content as string
    """
    sources_dir = os.path.abspath(settings.SOURCES_DIR)
    full_path = os.path.normpath(os.path.join(sources_dir, file_path))

    # Security: prevent path traversal
    if not full_path.startswith(sources_dir):
        raise ValueError(f"Path traversal not allowed: {file_path}")

    if not os.path.isfile(full_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(full_path, encoding="utf-8", errors="replace") as f:
        return f.read()
