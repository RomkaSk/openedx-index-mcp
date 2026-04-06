"""OpenEdX Index MCP Server — entry point."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP

from . import settings
from .services import bootstrap
from .tools import register_tools

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_server: FastMCP) -> AsyncIterator[None]:
    """Initialize code-index-mcp services on startup."""
    logger.info("Starting OpenEdX Index MCP server...")
    bootstrap.initialize()
    logger.info("Server ready.")
    yield
    logger.info("Server shutting down.")


mcp = FastMCP(
    "openedx-index",
    instructions="Search and analyze the full Open edX codebase (62 repos, 11k+ files)",
    lifespan=lifespan,
    host=settings.HOST,
    port=settings.PORT,
)

register_tools(mcp)


def main():
    """Run the MCP server."""
    logger.info(
        f"Config: sources={settings.SOURCES_DIR}, index={settings.INDEX_DIR}, "
        f"port={settings.PORT}"
    )
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
