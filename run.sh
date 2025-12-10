#!/bin/bash

# StudyBuddy Telegram Bot - Startup Script
# This script simplifies running the bot with proper environment setup

set -e  # Exit on error

echo "🚀 Starting StudyBuddy Telegram Bot..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "⚠️  Warning: Python $PYTHON_VERSION detected. Python $REQUIRED_VERSION+ recommended"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/bin/aiogram" ] && [ ! -f "venv/Scripts/aiogram" ]; then
    echo "📥 Installing dependencies..."
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    echo "✅ Dependencies installed"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo ""
    echo "Please create a .env file with your bot configuration:"
    echo "  1. Copy .env.example to .env"
    echo "  2. Add your BOT_TOKEN from @BotFather"
    echo ""
    echo "Quick setup:"
    echo "  cp .env.example .env"
    echo "  nano .env  # Edit and add your BOT_TOKEN"
    echo ""
    exit 1
fi

# Check if BOT_TOKEN is set
if ! grep -q "BOT_TOKEN=.*[^=]" .env; then
    echo "❌ Error: BOT_TOKEN not configured in .env file"
    echo ""
    echo "Please edit .env and add your bot token:"
    echo "  BOT_TOKEN=your_actual_token_here"
    echo ""
    exit 1
fi

echo "✅ Configuration verified"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  StudyBuddy Bot is starting..."
echo "  Press Ctrl+C to stop"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the bot
python main.py
