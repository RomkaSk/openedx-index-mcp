"""Index management tools."""

import os
from typing import Any

from code_index_mcp.services.index_management_service import IndexManagementService

from ..services.bootstrap import get_ctx, get_deep_manager
from .. import settings


def index_status() -> dict[str, Any]:
    """
    Get index health information.

    Returns:
        Dict with file_count, index_exists, index_size_mb, repos_indexed, stats
    """
    deep_mgr = get_deep_manager()

    stats = deep_mgr.get_index_stats()

    # Check index file size on disk
    sources_dir = os.path.abspath(settings.SOURCES_DIR)
    index_dir = os.path.abspath(settings.INDEX_DIR)

    index_size_mb = 0.0
    for root, _dirs, files in os.walk(index_dir):
        for f in files:
            fp = os.path.join(root, f)
            index_size_mb += os.path.getsize(fp)
    index_size_mb = round(index_size_mb / (1024 * 1024), 2)

    # Count repos (top-level dirs inside category dirs)
    repos = []
    for category in os.listdir(sources_dir):
        category_path = os.path.join(sources_dir, category)
        if os.path.isdir(category_path):
            for repo in os.listdir(category_path):
                repo_path = os.path.join(category_path, repo)
                if os.path.isdir(repo_path):
                    repos.append(f"{category}/{repo}")

    return {
        "sources_dir": sources_dir,
        "index_dir": index_dir,
        "index_size_mb": index_size_mb,
        "repos_indexed": repos,
        "repo_count": len(repos),
        "stats": stats,
    }


def rebuild_index() -> str:
    """
    Trigger a full re-index of all Open edX sources.

    This rebuilds both the shallow (file list) and deep (symbol) indexes.
    Takes several minutes for the full codebase.

    Returns:
        Status message
    """
    ctx = get_ctx()
    return IndexManagementService(ctx).rebuild_deep_index()
