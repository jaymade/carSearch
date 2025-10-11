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

# Copy environment template
if [ ! -f .env ]; then
    echo "⚙️  Creating environment configuration..."
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "🔑 IMPORTANT: Please edit the .env file and add your Twilio credentials:"
    echo "   1. Sign up at https://www.twilio.com"
    echo "   2. Get your Account SID and Auth Token from the Twilio Console"
    echo "   3. Purchase a phone number for sending SMS"
    echo "   4. Update the .env file with your credentials"
    echo ""
else
    echo "⚠️  .env file already exists, skipping..."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your .env file with Twilio credentials"
echo "2. Test SMS: python main.py --test-sms"
echo "3. Run a test search: python main.py --search-now"
echo "4. Start the scheduler: python main.py"
echo ""
echo "For help: python main.py --help"