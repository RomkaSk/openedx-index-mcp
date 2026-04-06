#!/bin/bash
# Clone Open edX ecosystem modules organized by category.
# Each repo is checked out at the tag matching the version in edx-platform requirements.
# Usage: ./clone_openedx.sh
#
# If a directory already exists, it is skipped (idempotent).
# Failed clones are logged but do not stop the script.

SOURCES_DIR="$(cd "$(dirname "$0")" && pwd)"
GITHUB="https://github.com"
FAILED=()

clone_repo() {
    local dir="$1"
    local org="$2"
    local repo="$3"
    local tag="$4"
    local target="${SOURCES_DIR}/${dir}/${repo}"

    if [ -d "$target" ]; then
        echo "SKIP (exists): ${dir}/${repo}"
        return 0
    fi

    mkdir -p "${SOURCES_DIR}/${dir}"

    # Try: exact tag -> v-prefixed tag -> default branch
    if git clone --depth 1 --branch "$tag" "${GITHUB}/${org}/${repo}.git" "$target" 2>/dev/null; then
        echo "  OK: ${org}/${repo} @ ${tag}"
    elif git clone --depth 1 --branch "v${tag}" "${GITHUB}/${org}/${repo}.git" "$target" 2>/dev/null; then
        echo "  OK: ${org}/${repo} @ v${tag}"
    elif git clone --depth 1 "${GITHUB}/${org}/${repo}.git" "$target" 2>/dev/null; then
        echo "  OK: ${org}/${repo} @ default branch (tag ${tag} not found)"
    else
        echo "  FAILED: ${org}/${repo}"
        FAILED+=("${org}/${repo}@${tag}")
    fi
}

echo "=== Cloning Open edX ecosystem modules ==="
echo ""

###############################################################################
# Platform
###############################################################################
echo "--- Platform ---"

clone_repo "common" "openedx" "openedx-platform"          "open-release/teak.3"

echo ""

###############################################################################
# Core Libraries (edx-*)
###############################################################################
echo "--- Core Libraries (edx-*) ---"

clone_repo "core-libraries" "openedx" "edx-ace"                    "1.11.4"
clone_repo "core-libraries" "openedx" "api-doc-tools"              "2.0.0"
clone_repo "core-libraries" "openedx" "auth-backends"              "4.5.0"
clone_repo "core-libraries" "openedx" "edx-bulk-grades"            "1.1.0"
clone_repo "core-libraries" "openedx" "ccx-keys"                   "2.0.2"
clone_repo "core-libraries" "openedx" "edx-celeryutils"            "1.3.0"
clone_repo "core-libraries" "openedx" "codejail"                   "3.5.2"
clone_repo "core-libraries" "openedx" "completion"                 "4.7.11"
clone_repo "core-libraries" "openedx" "edx-django-release-util"    "1.4.0"
clone_repo "core-libraries" "openedx" "edx-django-sites-extensions" "4.2.0"
clone_repo "core-libraries" "openedx" "edx-django-utils"           "7.4.0"
clone_repo "core-libraries" "openedx" "edx-drf-extensions"         "10.6.0"
clone_repo "core-libraries" "openedx" "edx-enterprise"             "5.12.7"
clone_repo "core-libraries" "openedx" "event-bus-kafka"            "6.1.0"
clone_repo "core-libraries" "openedx" "event-bus-redis"            "0.6.1"
clone_repo "core-libraries" "openedx" "i18n-tools"                 "1.5.0"
clone_repo "core-libraries" "openedx" "edx-milestones"             "0.6.0"
clone_repo "core-libraries" "edx"     "edx-name-affirmation"       "3.0.1"
clone_repo "core-libraries" "openedx" "opaque-keys"                "3.0.0"
clone_repo "core-libraries" "openedx" "edx-organizations"          "6.13.0"
clone_repo "core-libraries" "openedx" "edx-proctoring"             "5.1.2"
clone_repo "core-libraries" "openedx" "edx-rbac"                   "1.10.0"
clone_repo "core-libraries" "openedx" "edx-rest-api-client"        "6.2.0"
clone_repo "core-libraries" "openedx" "edx-search"                 "4.1.3"
clone_repo "core-libraries" "openedx" "edx-submissions"            "3.10.0"
clone_repo "core-libraries" "openedx" "edx-toggles"                "5.3.0"
clone_repo "core-libraries" "openedx" "edx-when"                   "2.5.1"
clone_repo "core-libraries" "openedx" "edx-val"                    "2.10.0"

echo ""

###############################################################################
# Core Libraries (openedx-*)
###############################################################################
echo "--- Core Libraries (openedx-*) ---"

clone_repo "core-libraries" "openedx" "openedx-atlas"              "0.7.0"
clone_repo "core-libraries" "openedx" "openedx-calc"               "4.0.2"
clone_repo "core-libraries" "openedx" "django-pyfs"                "3.7.0"
clone_repo "core-libraries" "openedx" "django-require"             "2.1.0"
clone_repo "core-libraries" "openedx" "django-wiki"                "2.1.0"
clone_repo "core-libraries" "openedx" "openedx-events"             "10.2.0"
clone_repo "core-libraries" "openedx" "openedx-filters"            "2.0.1"
# openedx-forum lives at openedx/forum (cloned above under core-libraries)
clone_repo "core-libraries" "openedx" "openedx-learning"           "0.26.0"
clone_repo "core-libraries" "openedx" "MongoDBProxy"               "0.2.2"
clone_repo "core-libraries" "openedx" "forum"                      "0.3.6"

echo ""

###############################################################################
# XBlocks
###############################################################################
echo "--- XBlocks ---"

clone_repo "xblocks" "openedx" "XBlock"                    "5.2.0"
clone_repo "xblocks" "openedx" "xblock-utils"              "4.0.0"
clone_repo "xblocks" "openedx" "acid-block"                "0.4.1"
clone_repo "xblocks" "openedx" "crowdsourcehinter"          "0.8"
clone_repo "xblocks" "openedx" "DoneXBlock"                "2.5.0"
clone_repo "xblocks" "openedx" "xblock-lti-consumer"       "9.13.4"
clone_repo "xblocks" "openedx" "edx-ora2"                  "6.16.1"
clone_repo "xblocks" "openedx" "RecommenderXBlock"         "3.0.0"
clone_repo "xblocks" "openedx" "staff_graded-xblock"       "3.0.1"
clone_repo "xblocks" "openedx" "xblock-drag-and-drop-v2"   "5.0.2"
clone_repo "xblocks" "openedx" "xblock-google-drive"       "0.8.1"
clone_repo "xblocks" "open-craft" "xblock-poll"             "1.14.1"
clone_repo "xblocks" "openedx" "xblocks-contrib"           "0.3.0"
clone_repo "xblocks" "mitodl"  "edx-sga"                   "0.25.3"

echo ""

###############################################################################
# Utilities & Support
###############################################################################
echo "--- Utilities ---"

clone_repo "utilities" "openedx" "code-annotations"         "2.3.0"
clone_repo "utilities" "openedx" "event-tracking"           "3.0.0"
clone_repo "utilities" "openedx" "help-tokens"              "3.1.0"
clone_repo "utilities" "openedx" "olxcleaner"               "0.3.0"
clone_repo "utilities" "openedx" "super-csv"                "4.0.1"
clone_repo "utilities" "openedx" "user-util"                "1.1.0"
clone_repo "utilities" "openedx" "web-fragments"            "3.0.0"
clone_repo "utilities" "openedx" "xss-utils"                "0.7.1"
clone_repo "utilities" "openedx" "django-config-models"     "2.9.0"

echo ""
echo "=== Done ==="
echo ""

if [ ${#FAILED[@]} -gt 0 ]; then
    echo "FAILED repos (${#FAILED[@]}):"
    for f in "${FAILED[@]}"; do
        echo "  - $f"
    done
    echo ""
fi

echo "Directory structure:"
echo "  sources/"
echo "  ├── common/openedx-platform  (already present)"
echo "  ├── core-libraries/          (~38 repos)"
echo "  ├── xblocks/                 (~14 repos)"
echo "  └── utilities/               (~9 repos)"
