# OpenEdX Index MCP

> **Supported version: Open edX Teak (open-release/teak.3)**
> All indexed repositories are pinned to versions matching the Teak release.

MCP server that provides search and analysis across the full Open edX codebase (62 repos, 11k+ files, 64k+ symbols) without requiring local clones.

## What it does

Developers working on Open edX plugins via Tutor only have their plugin code locally. This MCP server indexes the entire Open edX ecosystem and serves it over SSE so Claude Code can search, read, and understand the platform codebase.

## Tools

### Code tools

| Tool | Description |
|---|---|
| `search_code(pattern, case_sensitive?, file_pattern?, context_lines?, max_results?)` | Full-text/regex search across all repos |
| `find_files(pattern)` | Glob pattern file search (e.g., `**/models.py`) |
| `get_file_summary(file_path)` | Symbols, imports, exports for a file |
| `get_symbol_body(file_path, symbol_name)` | Extract function/class source code |
| `get_file_content(file_path)` | Read any file from the indexed sources |
| `index_status()` | Index health: file count, size, repos |
| `rebuild_index()` | Trigger full re-index |

### Documentation tools

| Tool | Description |
|---|---|
| `search_docs(query, doc_type?, max_results?)` | Search across all RST/MD documentation |
| `list_docs(doc_type?, repo?)` | Browse docs by type (`adr`, `how-to`, `reference`, `readme`, `changelog`, `guide`) or repo |
| `get_doc(path)` | Read full content of a documentation file |

## Setup

### Connect to existing server

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "openedx-index": {
      "type": "sse",
      "url": "http://your-server:8080/sse"
    }
  }
}
```

### Run locally

```bash
# Install
pip install -e ./code-index-mcp
pip install -e ./openedx-index-mcp

# Run (sources must be cloned first)
SOURCES_DIR=./sources INDEX_DIR=./index openedx-index-mcp
```

### Run with Docker

```bash
cd openedx-index-mcp
docker compose up --build
```

This clones all 62 repos during build, builds the index on first run, and serves on port 8080. The index is persisted via Docker volume.

## Indexed repositories

62 repos across 4 categories, pinned to specific release tags:

- **common/** -- `openedx-platform` (open-release/teak.3)
- **core-libraries/** -- 38 repos (edx-django-utils, openedx-events, openedx-filters, edx-enterprise, etc.)
- **xblocks/** -- 14 repos (XBlock, xblock-lti-consumer, edx-ora2, etc.)
- **utilities/** -- 9 repos (event-tracking, django-config-models, code-annotations, etc.)

## CLAUDE.md instructions

Add the following to your project's `CLAUDE.md` to teach Claude Code how to use this MCP:

```markdown
## Open edX Codebase Reference (Teak release)

You have access to the full Open edX Teak codebase (62 repos, 11k+ files) via the `openedx-index` MCP server. Use it whenever you need to understand Open edX internals, APIs, patterns, or conventions. All code and docs are from the Teak release.

### When to use

- Before implementing any Open edX plugin hook, signal handler, or filter pipeline
- When you need to understand how a Django model, view, or API works in edx-platform
- When looking for examples of how other apps/plugins implement something
- When you need to find the correct import path for an Open edX module
- When checking what events, signals, or filters are available
- When understanding architectural decisions behind a feature

### How to use

**Find code patterns:**
- `search_code("class CourseEnrollment", file_pattern="*.py")` -- find where a class is defined
- `search_code("ENROLLMENT_CREATED", file_pattern="*.py")` -- find signal/event usage
- `find_files("**/models.py")` -- find all model files across repos

**Understand a file or symbol:**
- `get_file_summary("common/openedx-platform/lms/djangoapps/courseware/models.py")` -- see all classes/functions
- `get_symbol_body("common/openedx-platform/lms/djangoapps/courseware/models.py", "StudentModule")` -- get full class source
- `get_file_content("common/openedx-platform/openedx/core/djangoapps/content/course_overviews/models.py")` -- read entire file

**Read documentation and ADRs:**
- `list_docs(doc_type="adr")` -- browse all Architecture Decision Records
- `list_docs(repo="core-libraries/openedx-events")` -- see all docs for a specific library
- `search_docs("enrollment", doc_type="adr")` -- find ADRs about enrollment
- `search_docs("filter pipeline", doc_type="how-to")` -- find how-to guides
- `get_doc("core-libraries/openedx-events/docs/decisions/0004-external-event-bus-and-django-signal-events.rst")` -- read a specific ADR

**Check index health:**
- `index_status()` -- verify the index is loaded and see repo count

### File paths

All paths are relative to the sources root. The structure is:
- `common/openedx-platform/` -- the main edx-platform monolith
- `core-libraries/{repo-name}/` -- edx-* and openedx-* packages
- `xblocks/{repo-name}/` -- XBlock implementations
- `utilities/{repo-name}/` -- support libraries

### Tips

- Always check the Open edX codebase before making assumptions about how something works
- Use `list_docs(doc_type="adr")` to find architectural decisions before designing new features
- Use `search_code` with `file_pattern="*.py"` to narrow results to Python files
- When implementing filters or event handlers, search for existing examples first
- The `get_file_summary` tool shows all symbols in a file -- use it to orient yourself before diving into specific functions
```
