#!/usr/bin/env bash
# Bootstrap script for local development

echo "Bootstrapping VisualResearcher..."

# 1. Setup upstream autoresearch deps
echo "Setting up upstream dependencies..."
if command -v uv &> /dev/null; then
    uv sync
else
    echo "Please install uv: https://github.com/astral-sh/uv"
    exit 1
fi

# 2. Add backend deps if any exist
# Example: cd app/backend && uv pip install -r requirements.txt (Claude to implement)
echo "Backend bootstrap pending implementation by Claude..."

# 3. Setup frontend
echo "Setting up frontend dependencies..."
cd app/frontend || exit
if command -v npm &> /dev/null; then
    npm install
else
    echo "Please install Node.js / npm"
    exit 1
fi

echo "Bootstrap complete! You can run ./scripts/dev.sh"
