# Stage 1: Clone Open edX repos
FROM alpine/git:latest AS clone

RUN apk add --no-cache bash

# Copy clone script into the target sources directory so SOURCES_DIR resolves correctly
COPY sources/clone_openedx.sh /data/sources/clone_openedx.sh
RUN chmod +x /data/sources/clone_openedx.sh && \
    cd /data/sources && \
    bash clone_openedx.sh

# Stage 2: Runtime
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ripgrep \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install code-index-mcp
COPY code-index-mcp/ /app/code-index-mcp/
RUN pip install --no-cache-dir /app/code-index-mcp/

# Install our package
COPY openedx-index-mcp/ /app/openedx-index-mcp/
RUN pip install --no-cache-dir /app/openedx-index-mcp/

# Copy cloned sources from stage 1
COPY --from=clone /data/sources /data/sources

# Create index directory
RUN mkdir -p /data/index

ENV SOURCES_DIR=/data/sources
ENV INDEX_DIR=/data/index
ENV PORT=8080

EXPOSE 8080

CMD ["openedx-index-mcp"]
