"""
Bootstrap code-index-mcp services for the OpenEdX index.

Creates a fake MCP context compatible with code-index-mcp's ContextHelper,
initializes ProjectSettings with our configured paths, and holds shared
service state as module-level singletons.
"""

import logging
import os
from dataclasses import dataclass, field
from typing import Optional

from code_index_mcp.project_settings import ProjectSettings
from code_index_mcp.indexing import get_index_manager, get_shallow_index_manager
from code_index_mcp.indexing.deep_index_manager import DeepIndexManager

from .. import settings

logger = logging.getLogger(__name__)


@dataclass
class LifespanContext:
    """Fake lifespan context matching CodeIndexerContext interface."""

    base_path: str = ""
    settings: Optional[ProjectSettings] = None
    file_count: int = 0
    file_watcher_service: object = None
    index_manager: object = None


@dataclass
class RequestContext:
    """Fake request context wrapping lifespan context."""

    lifespan_context: LifespanContext = field(default_factory=LifespanContext)


class FakeContext:
    """
    Fake MCP Context that satisfies code-index-mcp's ContextHelper.

    ContextHelper reads:
      - ctx.request_context.lifespan_context.base_path
      - ctx.request_context.lifespan_context.settings
      - ctx.request_context.lifespan_context.file_count
      - ctx.request_context.lifespan_context.index_manager
    """

    def __init__(self, lifespan_ctx: LifespanContext):
        self.request_context = RequestContext(lifespan_context=lifespan_ctx)


# Module-level shared state
_ctx: Optional[FakeContext] = None
_deep_manager: Optional[DeepIndexManager] = None


def get_ctx() -> FakeContext:
    """Return the shared fake context. Must call initialize() first."""
    if _ctx is None:
        raise RuntimeError("Bootstrap not initialized. Call initialize() first.")
    return _ctx


def initialize() -> FakeContext:
    """
    Initialize code-index-mcp services with pre-configured paths.

    1. Set custom_index_root so index is stored in our persistent directory
    2. Create ProjectSettings for the sources directory
    3. Initialize shallow index (file list)
    4. Load or build deep index
    5. Store everything in a fake context for services to use

    Returns:
        The initialized FakeContext
    """
    global _ctx, _deep_manager

    sources_dir = os.path.abspath(settings.SOURCES_DIR)
    index_dir = os.path.abspath(settings.INDEX_DIR)

    logger.info(f"Initializing with sources={sources_dir}, index={index_dir}")

    # Ensure directories exist
    os.makedirs(index_dir, exist_ok=True)

    if not os.path.isdir(sources_dir):
        raise RuntimeError(f"Sources directory does not exist: {sources_dir}")

    # Configure code-index-mcp to store index in our persistent directory
    ProjectSettings.custom_index_root = index_dir

    # Create project settings for the sources directory
    project_settings = ProjectSettings(base_path=sources_dir, skip_load=False)

    # Create lifespan context
    lifespan_ctx = LifespanContext(
        base_path=sources_dir,
        settings=project_settings,
    )
    _ctx = FakeContext(lifespan_ctx)

    # Initialize shallow index manager
    shallow_mgr = get_shallow_index_manager()
    if not shallow_mgr.set_project_path(sources_dir):
        raise RuntimeError(f"Failed to set shallow index project path: {sources_dir}")

    if shallow_mgr.load_index():
        logger.info("Loaded existing shallow index")
    else:
        logger.info("Building new shallow index...")
        if not shallow_mgr.build_index():
            raise RuntimeError("Failed to build shallow index")
        logger.info("Shallow index built")

    file_count = len(shallow_mgr.get_file_list())
    lifespan_ctx.file_count = file_count
    logger.info(f"Shallow index: {file_count} files")

    # Initialize deep index manager
    _deep_manager = DeepIndexManager()
    _deep_manager.set_project_path(sources_dir)

    # Store index manager in context for services
    index_mgr = get_index_manager()
    index_mgr.set_project_path(sources_dir)
    lifespan_ctx.index_manager = index_mgr

    # Try to load existing deep index
    if _deep_manager.load_index():
        stats = _deep_manager.get_index_stats()
        logger.info(f"Loaded existing deep index: {stats}")
    else:
        logger.info("No existing deep index found. Building (this may take a while)...")
        _deep_manager.build_index()
        stats = _deep_manager.get_index_stats()
        logger.info(f"Deep index built: {stats}")

    return _ctx


def get_deep_manager() -> DeepIndexManager:
    """Return the shared DeepIndexManager."""
    if _deep_manager is None:
        raise RuntimeError("Bootstrap not initialized. Call initialize() first.")
    return _deep_manager
