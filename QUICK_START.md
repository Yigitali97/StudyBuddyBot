# ⚡ Quick Start Guide

Get your StudyBuddy bot running in **5 minutes**!

## 🎯 Prerequisites

- Python 3.11+ installed
- A Telegram account

## 🚀 Setup in 5 Steps

### 1️⃣ Get Your Bot Token (2 minutes)

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the prompts
3. Copy the bot token (looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2️⃣ Install Dependencies (1 minute)

```bash
# Navigate to project directory
cd StudyBuddy

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt
```

### 3️⃣ Configure Bot (30 seconds)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your token
nano .env
# Or use any text editor
```

Add this line to `.env`:
```
BOT_TOKEN=your_actual_bot_token_here
```

Save and exit.

### 4️⃣ Run the Bot (10 seconds)

```bash
python main.py
```

You should see:
```
Bot started: @your_bot_username
Starting polling...
```

### 5️⃣ Test It! (1 minute)

1. Open Telegram
2. Search for your bot username
3. Send `/start`
4. Try adding a task with `/add`

## ✅ You're Done!

Your bot is now running! Keep the terminal open while using it.

## 📱 Basic Usage

### 🎮 Using Buttons (Easiest!)

When you open the bot, you'll see **4 buttons** at the bottom:
```
┌─────────────────────────────────┐
│  ➕ Add Task    📋 List Tasks   │
│  🗑️ Delete Task   ❓ Help       │
└─────────────────────────────────┘
```

**Just tap the buttons to use the bot - no commands needed!**

### Add a Task
```
[Tap ➕ Add Task button]
→ Tap "Assignment" or "Exam" button
→ Enter task name: "Math Homework Chapter 5"
→ Enter due date: "25/12/2025"
→ Done! ✅
```

### View Tasks
```
[Tap 📋 List Tasks button]
→ See all upcoming deadlines
```

### Delete a Task
```
[Tap 🗑️ Delete Task button]
→ Type task number
→ Tap Yes/No to confirm deletion
```

### Using Commands (Alternative)
You can also type commands if you prefer:
- `/add` - Add task
- `/list` - View tasks
- `/delete` - Delete task
- `/help` - Get help

## 🛑 Stop the Bot

Press `Ctrl + C` in the terminal

## 🆘 Having Issues?

### Bot doesn't start?
- Check `BOT_TOKEN` in `.env` file
- Make sure virtual environment is activated

### Bot doesn't respond?
- Ensure bot is running (check terminal)
- Try `/start` command first

### Import errors?
```bash
pip install -r requirements.txt --force-reinstall
```

## 📚 Next Steps

- Read [SETUP.md](SETUP.md) for detailed setup
- Check [README.md](README.md) for full documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) for hosting options

## 🎉 Features

✨ **What Your Bot Can Do:**
- 📝 Track assignments and exams
- 📅 Sort tasks by due date
- ⏰ Send reminders 24 hours before deadlines
- 🗑️ Delete completed tasks
- 💬 User-friendly conversation flow

## 🔧 Quick Reference

### Buttons (Always Visible)
| Button | What it does |
|--------|-------------|
| ➕ Add Task | Create new task |
| 📋 List Tasks | View all tasks |
| 🗑️ Delete Task | Remove task |
| ❓ Help | Show help |

### Commands (Alternative)
| Command | What it does |
|---------|-------------|
| `/start` | Start the bot |
| `/add` | Add new task |
| `/list` | View all tasks |
| `/delete` | Remove task |
| `/help` | Show help |
| `/cancel` | Cancel current action |

💡 **New users:** Just use the buttons - they're easier!

## 💡 Pro Tips

1. **Use buttons**: Tap the buttons instead of typing commands - it's faster!
2. **Keep bot running**: Use `screen` or `tmux` for persistent sessions
3. **Deploy online**: Check DEPLOYMENT.md for free hosting on Render.com
4. **Backup database**: Copy `studybuddy.db` file regularly
5. **Monitor logs**: Check terminal for any errors
6. **Button guide**: See BUTTONS_GUIDE.md for detailed button usage

## 🚀 One-Liner Setup (macOS/Linux)

```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && echo "Now edit .env with your BOT_TOKEN, then run: python main.py"
```

---

## 🎉 No Commands to Remember!

**The button interface makes StudyBuddy super easy:**
- ✅ Just tap buttons
- ✅ No typing needed
- ✅ Perfect for mobile
- ✅ Beginner-friendly

**Made with ❤️ for students**

Need help? Tap the ❓ Help button or check BUTTONS_GUIDE.md!