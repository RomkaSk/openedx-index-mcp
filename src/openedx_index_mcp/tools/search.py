"""Search tools: search_code and find_files."""

from typing import Any, Optional

from code_index_mcp.services.search_service import SearchService
from code_index_mcp.services.file_discovery_service import FileDiscoveryService

from ..services.bootstrap import get_ctx


def search_code(
    pattern: str,
    case_sensitive: bool = True,
    context_lines: int = 0,
    file_pattern: Optional[str] = None,
    max_results: int = 10,
) -> dict[str, Any]:
    """
    Search across all Open edX repositories.

    Args:
        pattern: Search pattern (text or regex)
        case_sensitive: Whether search is case-sensitive
        context_lines: Number of context lines around matches
        file_pattern: Glob to filter files (e.g., "*.py")
        max_results: Maximum results to return (default 10)

    Returns:
        Dict with 'results' list and 'pagination' info
    """
    ctx = get_ctx()
    return SearchService(ctx).search_code(
        pattern=pattern,
        case_sensitive=case_sensitive,
        context_lines=context_lines,
        file_pattern=file_pattern,
        max_results=max_results,
    )


def find_files(pattern: str) -> list[str]:
    """
    Find files matching a glob pattern across all Open edX repositories.

    Args:
        pattern: Glob pattern (e.g., "**/models.py", "*.ts")

    Returns:
        List of matching file paths relative to sources root
    """
    ctx = get_ctx()
    return FileDiscoveryService(ctx).find_files(pattern)
