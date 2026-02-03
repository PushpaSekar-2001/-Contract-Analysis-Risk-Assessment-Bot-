#!/bin/bash
# GenAI Contract Analysis Bot - macOS/Linux Setup Script

echo ""
echo "==================================================="
echo "  GenAI Contract Analysis & Risk Assessment Bot"
echo "  Setup Script for macOS/Linux"
echo "==================================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install requirements
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "✓ All dependencies installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  IMPORTANT: Create a .env file in the project root"
    echo ""
    echo "Steps:"
    echo "1. Go to https://console.anthropic.com/api_keys"
    echo "2. Create an API key"
    echo "3. Create a file named .env in the project folder"
    echo "4. Add: ANTHROPIC_API_KEY=your-key-here"
    echo ""
    echo "You can use .env.example as a template"
    echo ""
fi

echo ""
echo "==================================================="
echo "  Setup Complete! ✓"
echo "==================================================="
echo ""
echo "To start the application:"
echo "  streamlit run app.py"
echo ""
echo "The app will open at: http://localhost:8501"
echo ""
