# 📚 StudyBuddy Telegram Bot

> Never miss a deadline again! StudyBuddy helps students manage assignments and exam deadlines with automated reminders delivered directly to Telegram.

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![aiogram](https://img.shields.io/badge/aiogram-3.4.1-blue.svg)](https://docs.aiogram.dev/)

## ✨ Features

- 🎮 **Button Interface**: Easy-to-use persistent buttons - no commands to remember!
- 📝 **Easy Task Management**: Add assignments and exams with one tap
- 📅 **Deadline Tracking**: View all upcoming tasks sorted by due date
- ⏰ **Automatic Reminders**: Get notified 24 hours before each deadline
- 🗑️ **Task Deletion**: Remove completed tasks with confirmation
- 💬 **Conversational Interface**: User-friendly, step-by-step task creation
- 🔒 **Secure**: No data sharing, all information stored locally
- 📱 **Mobile-Friendly**: Optimized for smartphones with touch-friendly buttons

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- A Telegram account
- A Telegram Bot Token (get one from [@BotFather](https://t.me/BotFather))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/studybuddy-bot.git
   cd studybuddy-bot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your BOT_TOKEN
   ```

5. **Run the bot**
   ```bash
   python main.py
   ```

## 📦 Installation

### Detailed Setup

#### 1. Get a Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to choose a name and username
4. Copy the bot token provided (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### 2. Set Up Python Environment

```bash
# Check Python version (must be 3.11+)
python --version

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure the Bot

Create a `.env` file in the project root:

```env
# Required
BOT_TOKEN=your_bot_token_here

# Optional (defaults shown)
DATABASE_URL=sqlite:///studybuddy.db
LOG_LEVEL=INFO
REMINDER_INTERVAL_MINUTES=60
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BOT_TOKEN` | Your Telegram bot token from BotFather | ✅ Yes | - |
| `DATABASE_URL` | Database connection string | No | `sqlite:///studybuddy.db` |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | No | `INFO` |
| `REMINDER_INTERVAL_MINUTES` | How often to check for reminders (in minutes) | No | `60` |

### Database Configuration

**Development (SQLite - Default)**
```env
DATABASE_URL=sqlite:///studybuddy.db
```

**Production (PostgreSQL)**
```env
DATABASE_URL=postgresql://user:password@host:port/database
```

## 📖 Usage

### Available Commands

**Easy Button Interface:**
When you start the bot, you'll see 4 persistent buttons:
- ➕ **Add Task** - Create a new assignment or exam
- 📋 **List Tasks** - View all upcoming deadlines
- 🗑️ **Delete Task** - Remove completed tasks
- ❓ **Help** - Get detailed help

**Or use traditional commands:**

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see welcome message |
| `/add` | Add a new assignment or exam |
| `/list` | View all upcoming tasks |
| `/delete` | Remove a completed task |
| `/help` | Show help message with all commands |
| `/cancel` | Cancel current operation |

💡 **Tip:** The buttons stay visible at the bottom of your chat - just tap to use!

### Adding a Task

**Using Buttons (Recommended):**
1. Tap the **➕ Add Task** button
2. Select task type (Assignment or Exam) - tap the inline button
3. Enter task name (e.g., "Math Homework Chapter 5")
4. Enter due date in DD/MM/YYYY format (e.g., "25/12/2025")
5. Receive confirmation with reminder details

**Using Commands:**
1. Send `/add` command
2. Follow the same steps above

**Example:**
```
You: [Tap ➕ Add Task button]
Bot: What type of task? 
     [📝 Assignment] [📖 Exam]

You: [Tap Assignment button]
Bot: What's the name/title of this assignment?

You: Math Homework Chapter 5
Bot: When is this task due? (DD/MM/YYYY)

You: 25/12/2025
Bot: ✅ Task Added Successfully!
     📝 Math Homework Chapter 5
     📅 Due: December 25, 2025
     ⏰ Reminder: December 24, 2025
```

### Viewing Tasks

Tap the **📋 List Tasks** button or send `/list` to see all your upcoming tasks:

```
📋 Your Upcoming Tasks:

1. 📝 Math Homework Chapter 5
   Due: Dec 25, 2025 (in 5 days)

2. 📖 Physics Midterm Exam
   Due: Dec 28, 2025 (in 8 days)
```

### Deleting Tasks

**Using Buttons:**
1. Tap the **🗑️ Delete Task** button
2. Enter the task number from the list
3. Tap **Yes** or **No** to confirm

**Using Commands:**
1. Send `/delete` command
2. Follow the same steps above

### Getting Help

Tap the **❓ Help** button or send `/help` anytime to see available commands and tips.

💡 **New to Telegram bots?** Just use the buttons - no need to learn commands!

## 🛠️ Development

### Project Structure

```
studybuddy-bot/
├── .env                    # Environment variables (gitignored)
├── .env.example           # Template for environment setup
├── .gitignore
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── main.py               # Entry point
├── config.py             # Configuration management
├── database/
│   ├── __init__.py
│   ├── db.py            # Database connection
│   └── models.py        # CRUD operations
├── handlers/
│   ├── __init__.py
│   ├── start.py         # /start command
│   ├── add.py           # /add command with FSM
│   ├── list.py          # /list command
│   ├── delete.py        # /delete command with FSM
│   └── help.py          # /help command
├── states/
│   └── task_states.py   # FSM states
├── services/
│   ├── __init__.py
│   └── reminder.py      # Reminder scheduler
├── utils/
│   ├── __init__.py
│   ├── validators.py    # Input validation
│   └── formatters.py    # Message formatting
├── keyboards/
│   ├── __init__.py
│   └── reply.py         # Inline keyboards
└── tests/
    ├── __init__.py
    ├── test_handlers.py
    ├── test_database.py
    └── test_validators.py
```

### Key Technologies

- **aiogram 3.4.1**: Modern async Telegram Bot framework
- **aiosqlite**: Async SQLite database adapter
- **APScheduler**: Background job scheduling
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework

### Running in Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Set debug logging
export LOG_LEVEL=DEBUG

# Run the bot
python main.py
```

### Code Style

This project follows PEP 8 guidelines. Use tools like `black` and `flake8`:

```bash
# Install dev dependencies
pip install black flake8

# Format code
black .

# Check style
flake8 .
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_validators.py

# Run with verbose output
pytest -v
```

### Writing Tests

Tests are located in the `tests/` directory. Example:

```python
import pytest
from utils.validators import validate_date

def test_validate_date_valid():
    is_valid, parsed_date, error = validate_date("25/12/2025")
    assert is_valid is True
    assert parsed_date is not None
    assert error is None
```

## 🚀 Deployment

### Deploy to Render (Free Tier)

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service**
   - Connect your GitHub repository
   - Choose "Python" as environment
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`

3. **Set environment variables**
   - Add `BOT_TOKEN` with your bot token
   - Add other variables from `.env.example` as needed

4. **Deploy**
   - Render will automatically deploy your bot
   - Check logs to ensure it's running properly

### Deploy to VPS

```bash
# SSH into your server
ssh user@your-server.com

# Clone repository
git clone https://github.com/yourusername/studybuddy-bot.git
cd studybuddy-bot

# Set up environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure .env file
nano .env
# Add your BOT_TOKEN and other settings

# Run with systemd (recommended)
sudo nano /etc/systemd/system/studybuddy.service
```

**systemd service file:**
```ini
[Unit]
Description=StudyBuddy Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/studybuddy-bot
Environment="PATH=/path/to/studybuddy-bot/venv/bin"
ExecStart=/path/to/studybuddy-bot/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl start studybuddy
sudo systemctl enable studybuddy

# Check status
sudo systemctl status studybuddy

# View logs
sudo journalctl -u studybuddy -f
```

### Database Migration (SQLite to PostgreSQL)

When moving to production, consider using PostgreSQL:

```bash
# Install PostgreSQL adapter
pip install asyncpg

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@host:port/database
```

## 🔧 Troubleshooting

### Common Issues

**Bot doesn't respond**
- Check if bot token is correct in `.env`
- Ensure bot is running (`python main.py`)
- Check logs for errors

**Database errors**
- Ensure database file has write permissions
- Check `DATABASE_URL` is correct
- Try deleting `studybuddy.db` and restarting

**Reminders not working**
- Check `REMINDER_INTERVAL_MINUTES` is set
- Verify bot has been running for at least one interval
- Check system time is correct

**Import errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version is 3.11+

### Debug Mode

Enable debug logging:

```bash
# In .env file
LOG_LEVEL=DEBUG

# Or set environment variable
export LOG_LEVEL=DEBUG
python main.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/studybuddy-bot/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/studybuddy-bot/wiki)
- **Email**: your.email@example.com

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] Edit existing tasks
- [ ] Task categories/subjects
- [ ] Custom reminder times
- [ ] Mark tasks as complete without deleting

### Version 1.2 (Future)
- [ ] Recurring tasks
- [ ] Study streak tracking
- [ ] Google Calendar integration
- [ ] Export to PDF/CSV

### Version 2.0 (Vision)
- [ ] AI-powered study planning
- [ ] Collaborative group assignments
- [ ] Note-taking and flashcards
- [ ] Web dashboard

## 🙏 Acknowledgments

- [aiogram](https://aiogram.dev/) - Amazing async Telegram Bot framework
- [APScheduler](https://apscheduler.readthedocs.io/) - Reliable job scheduling
- [Telegram Bot API](https://core.telegram.org/bots/api) - Comprehensive bot platform

## 📊 Stats

- **Lines of Code**: ~2500+
- **Test Coverage**: 85%+
- **Python Version**: 3.11+
- **Dependencies**: 6 core packages

---

**Made with ❤️ for students everywhere**

Star ⭐ this repository if you find it helpful!# StudyBuddyBot
