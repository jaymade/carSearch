#!/bin/bash

# Honda Car Search App Installation Script

echo "🚗 Honda Car Search App Setup"
echo "================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "⬇️  Installing Python packages..."
pip install -r requirements.txt

# Create log file
echo "📄 Creating log file..."
touch search.log

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run a test search: python3 src/main.py --search-now"
echo "2. Check search statistics: python3 src/main.py --stats"
echo "3. Start the automated scheduler: python3 src/main.py"
echo "4. View web dashboard: https://[your-username].github.io/honda-car-search/"
echo ""
echo "For help: python3 src/main.py --help"