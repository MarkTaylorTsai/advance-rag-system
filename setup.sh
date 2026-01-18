#!/bin/bash
# Setup script for RAG System

set -e

echo "🚀 Setting up RAG System..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 not found. Please install Python 3.11 or later."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -e ./backend uvicorn

echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "Then you can run the server with:"
echo "  python3 run_server.py"

