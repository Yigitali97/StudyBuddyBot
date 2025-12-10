# 🚀 StudyBuddy Bot - Setup Guide

This guide will walk you through setting up and running the StudyBuddy Telegram bot from scratch.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11 or higher** installed on your system
- A **Telegram account**
- Basic knowledge of command line/terminal

## 🔧 Step-by-Step Setup

### Step 1: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start a chat with BotFather
3. Send the command: `/newbot`
4. Follow the prompts:
   - Choose a name for your bot (e.g., "StudyBuddy Helper")
   - Choose a username (must end in 'bot', e.g., "studybuddy_helper_bot")
5. **Save the bot token** - it looks like this:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
   ```
   ⚠️ **Keep this token secret!** Never commit it to Git.

### Step 2: Clone/Download the Project

```bash
cd ~/Documents
git clone <repository-url> StudyBuddy
cd StudyBuddy
```

Or if you have the files already:
```bash
cd ~/Documents/StudyBuddy
```

### Step 3: Create a Virtual Environment

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- `aiogram` - Telegram bot framework
- `aiosqlite` - Async SQLite database
- `APScheduler` - Background job scheduler
- `python-dotenv` - Environment variable manager
- `pytest` - Testing framework

### Step 5: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file:
   ```bash
   nano .env
   # or use your preferred text editor
   ```

3. Add your bot token:
   ```env
   BOT_TOKEN=your_actual_bot_token_here
   DATABASE_URL=sqlite:///studybuddy.db
   LOG_LEVEL=INFO
   REMINDER_INTERVAL_MINUTES=60
   ```

4. Save and close the file (Ctrl+X, then Y, then Enter in nano)

### Step 6: Verify the Setup

Check that all files are in place:
```bash
ls -la
```

You should see:
- `main.py` - Entry point
- `config.py` - Configuration
- `requirements.txt` - Dependencies
- `.env` - Your environment variables (should exist now)
- `.env.example` - Template
- Folders: `database/`, `handlers/`, `services/`, `utils/`, `keyboards/`, `states/`, `tests/`

### Step 7: Run the Bot

```bash
python main.py
```

If everything is configured correctly, you should see:
```
2024-12-10 02:45:30 - __main__ - INFO - Logging configured with level: INFO
2024-12-10 02:45:30 - database.db - INFO - Database manager initialized with path: studybuddy.db
2024-12-10 02:45:30 - __main__ - INFO - Bot is starting up...
2024-12-10 02:45:30 - database.db - INFO - Database connection established
2024-12-10 02:45:30 - database.db - INFO - Database schema initialized successfully
2024-12-10 02:45:30 - __main__ - INFO - Startup complete!
2024-12-10 02:45:30 - __main__ - INFO - All handlers registered
2024-12-10 02:45:30 - services.reminder - INFO - Reminder service initialized
2024-12-10 02:45:30 - services.reminder - INFO - Reminder service started. Checking every 60 minute(s)
2024-12-10 02:45:31 - __main__ - INFO - Bot started: @your_bot_username
2024-12-10 02:45:31 - __main__ - INFO - Starting polling...
```

### Step 8: Test the Bot

1. Open Telegram on your phone or desktop
2. Search for your bot username (e.g., `@studybuddy_helper_bot`)
3. Start a chat and send: `/start`
4. You should receive a welcome message!

Try these commands:
- `/help` - See all available commands
- `/add` - Add a new task
- `/list` - View your tasks
- `/delete` - Delete a task

## 🧪 Running Tests

To verify everything works correctly:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html
```

## 🐛 Troubleshooting

### Bot doesn't start

**Error: "BOT_TOKEN is not set"**
- Solution: Make sure you created `.env` file and added your bot token

**Error: "No module named 'aiogram'"**
- Solution: Activate virtual environment and install requirements:
  ```bash
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  pip install -r requirements.txt
  ```

**Error: "Database connection failed"**
- Solution: Check that you have write permissions in the current directory
- Try deleting `studybuddy.db` if it exists and restart

### Bot doesn't respond to commands

1. Check that the bot is running (no errors in terminal)
2. Make sure you're chatting with the correct bot
3. Try `/start` command first
4. Check terminal logs for errors

### Reminders not working

1. Ensure bot has been running for at least the reminder interval (default 60 minutes)
2. Check that tasks are created with future dates
3. Verify system time is correct
4. Look for errors in logs

### Import errors

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

## 📊 Project Structure Overview

```
StudyBuddy/
├── main.py              # ← Start here
├── config.py            # Configuration
├── .env                 # Your secrets (DO NOT COMMIT)
├── requirements.txt     # Dependencies
│
├── database/           # Database layer
│   ├── db.py          # Connection management
│   └── models.py      # CRUD operations
│
├── handlers/          # Command handlers
│   ├── start.py      # /start command
│   ├── help.py       # /help command
│   ├── add.py        # /add command
│   ├── list.py       # /list command
│   └── delete.py     # /delete command
│
├── services/         # Background services
│   └── reminder.py   # Reminder scheduler
│
├── utils/           # Utilities
│   ├── validators.py # Input validation
│   └── formatters.py # Message formatting
│
├── keyboards/       # UI keyboards
│   └── reply.py     # Inline keyboards
│
├── states/          # FSM states
│   └── task_states.py
│
└── tests/          # Unit tests
    └── test_validators.py
```

## 🔄 Stopping the Bot

To stop the bot safely:
1. Press `Ctrl+C` in the terminal
2. Wait for "Bot stopped by user" message
3. The bot will clean up and close database connections

## 🚀 Next Steps

Once your bot is running:

1. **Customize the bot**:
   - Edit welcome message in `handlers/start.py`
   - Adjust reminder interval in `.env`
   - Add custom commands

2. **Deploy to production**:
   - See `README.md` for deployment guides (Render, VPS, etc.)
   - Switch to PostgreSQL for production

3. **Monitor usage**:
   - Check logs regularly
   - Monitor database size
   - Set up alerts for errors

## 📚 Additional Resources

- [aiogram Documentation](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python asyncio Tutorial](https://docs.python.org/3/library/asyncio.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## 💡 Tips

- **Keep the bot running**: Use `screen` or `tmux` on Linux/macOS for persistent sessions
- **Backup database**: Regularly backup `studybuddy.db` file
- **Monitor logs**: Check logs daily for errors
- **Test changes**: Always test in development before deploying

## 🆘 Need Help?

- Check the logs in the terminal
- Review the `README.md` for more details
- Look at the test files for usage examples
- Open an issue on GitHub

---

**Happy coding! 🎉**

Made with ❤️ for students everywhere