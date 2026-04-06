"""Register all tools on a FastMCP app."""

from mcp.server.fastmcp import FastMCP

from . import search, symbols, index, docs


def register_tools(mcp: FastMCP) -> None:
    """Register all OpenEdX index tools on the given FastMCP app."""

    @mcp.tool()
    def search_code(
        pattern: str,
        case_sensitive: bool = True,
        context_lines: int = 0,
        file_pattern: str | None = None,
        max_results: int = 10,
    ) -> dict:
        """Search across all 62 Open edX repositories. Supports text and regex patterns."""
        return search.search_code(
            pattern=pattern,
            case_sensitive=case_sensitive,
            context_lines=context_lines,
            file_pattern=file_pattern,
            max_results=max_results,
        )

    @mcp.tool()
    def find_files(pattern: str) -> list[str]:
        """Find files matching a glob pattern across all Open edX repos (e.g., '**/models.py')."""
        return search.find_files(pattern)

    @mcp.tool()
    def get_file_summary(file_path: str) -> dict:
        """Get symbols, imports, and metadata for a file in the Open edX codebase."""
        return symbols.get_file_summary(file_path)

    @mcp.tool()
    def get_symbol_body(file_path: str, symbol_name: str) -> dict:
        """Get source code of a function, class, or method from the Open edX codebase."""
        return symbols.get_symbol_body(file_path, symbol_name)

    @mcp.tool()
    def get_file_content(file_path: str) -> str:
        """Read a file from the indexed Open edX sources."""
        return symbols.get_file_content(file_path)

    @mcp.tool()
    def index_status() -> dict:
        """Get index health: file count, size, repos indexed, symbol stats."""
        return index.index_status()

    @mcp.tool()
    def rebuild_index() -> str:
        """Trigger full re-index of all Open edX sources. Takes several minutes."""
        return index.rebuild_index()

    @mcp.tool()
    def search_docs(
        query: str,
        doc_type: str = "all",
        max_results: int = 10,
    ) -> dict:
        """Search across Open edX documentation, ADRs, how-to guides, and references."""
        return docs.search_docs(query=query, doc_type=doc_type, max_results=max_results)

    @mcp.tool()
    def list_docs(
        doc_type: str | None = None,
        repo: str | None = None,
    ) -> list[dict]:
        """List available Open edX docs. Filter by type (adr, how-to, reference, readme, changelog, guide) and/or repo (e.g., 'core-libraries/openedx-events')."""
        return docs.list_docs(doc_type=doc_type, repo=repo)

    @mcp.tool()
    def get_doc(path: str) -> str:
        """Read full content of an Open edX documentation file (RST or MD)."""
        return docs.get_doc(path)
