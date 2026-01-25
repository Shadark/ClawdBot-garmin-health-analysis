#!/bin/bash
# Installation script for Garmin Health Analysis skill

echo "🔧 Installing Garmin Health Analysis..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7+ first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Authenticate: python3 scripts/garmin_auth.py login --email YOUR_EMAIL --password YOUR_PASSWORD"
    echo "2. Test: python3 scripts/garmin_data.py summary --days 7"
    echo "3. Generate charts: python3 scripts/garmin_chart.py dashboard --days 30"
else
    echo "❌ Installation failed. Check error messages above."
    exit 1
fi
