#!/bin/bash
# Gemini AI Connector Installation Script

set -e  # Exit on any error

echo "🚀 Installing Gemini AI Connector..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8 or newer."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION or newer is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📋 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p config/user

# Copy configuration templates if they don't exist
if [ ! -f "config/user/.env" ]; then
    echo "⚙️  Setting up configuration..."
    cp config/.env.template config/user/.env
    echo "📝 Please edit config/user/.env with your Gemini API key"
fi

if [ ! -f "config/user/config.json" ]; then
    cp config/config.template.json config/user/config.json
    echo "📝 Please edit config/user/config.json with your settings"
fi

# Make scripts executable
chmod +x src/gemini_connector.py
chmod +x install.sh

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "Next steps:"
echo "1. Get your Gemini API key from: https://makersuite.google.com/app/apikey"
echo "2. Edit config/user/.env and add your API key"
echo "3. Test the connection: python3 src/gemini_connector.py --validate"
echo "4. Try interactive chat: python3 src/gemini_connector.py --chat"
echo ""
echo "For more information, see the documentation in docs/README.md"