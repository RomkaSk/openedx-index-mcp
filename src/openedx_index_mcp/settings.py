"""Configuration from environment variables."""

import os

SOURCES_DIR = os.environ.get("SOURCES_DIR", "/data/sources")
INDEX_DIR = os.environ.get("INDEX_DIR", "/data/index")
PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")
