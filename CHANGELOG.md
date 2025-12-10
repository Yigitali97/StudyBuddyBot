# Changelog

All notable changes to StudyBuddy Telegram Bot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-12-10

### 🎮 Added - Button Interface Update

#### New Features
- **Persistent Button Menu** - 4 main buttons now always visible at bottom of chat
  - ➕ Add Task button
  - 📋 List Tasks button
  - 🗑️ Delete Task button
  - ❓ Help button
- **Telegram Command Menu** - Commands now appear in Telegram's `/` menu
- **Button Text Handlers** - Bot responds to both button taps and typed commands
- **Input Field Placeholder** - Helpful placeholder text: "Choose an option or type a command..."
- **Auto-resize Keyboard** - Buttons automatically fit screen size on all devices

#### Documentation
- Added `BUTTONS_GUIDE.md` - Complete guide to button interface
- Updated `README.md` - Button interface prominently featured
- Updated `QUICK_START.md` - Button usage examples added
- Updated all handler files - Consistent button support

#### User Experience Improvements
- ✅ No need to remember commands anymore
- ✅ One-tap access to all features
- ✅ Perfect for mobile devices
- ✅ Beginner-friendly interface
- ✅ Commands still work for advanced users

#### Technical Changes
- Centralized `get_main_menu_keyboard()` function in `keyboards/reply.py`
- Added `F.text` filters to all command handlers
- Implemented `set_bot_commands()` in `main.py`
- All handlers now return main menu after operations
- Removed duplicate keyboard code across handlers

### 🔧 Changed
- Start message now emphasizes buttons over commands
- Help message updated to show button options first
- All confirmation messages now restore main menu
- Handler imports simplified using central keyboard module

### 📱 Mobile Optimization
- Buttons use `resize_keyboard=True` for optimal mobile display
- Persistent menu with `persistent=True` stays visible
- Large touch-friendly button areas
- Clear emoji icons for visual guidance

---

## [1.0.0] - 2024-12-10

### 🎉 Initial Release - MVP Complete

#### Core Features
- **Task Management**
  - `/start` - Welcome message and user registration
  - `/add` - Add assignments and exams with FSM flow
  - `/list` - View all upcoming tasks sorted by date
  - `/delete` - Remove tasks with confirmation
  - `/help` - Comprehensive help documentation
  - `/cancel` - Cancel current operation

- **Automated Reminders**
  - Background scheduler using APScheduler
  - 24-hour advance reminders
  - Automatic delivery via Telegram
  - Duplicate prevention system

- **Database**
  - SQLite for development
  - PostgreSQL-ready for production
  - User and Task models
  - Indexed queries for performance

- **Validation & Error Handling**
  - Date validation (DD/MM/YYYY format)
  - Title length and content validation
  - Task type validation
  - Comprehensive error messages
  - Input sanitization

- **User Experience**
  - Conversational FSM flows
  - Inline keyboards for selections
  - Relative time display ("in 3 days")
  - Emoji icons for visual clarity
  - Helpful error messages

#### Documentation
- `README.md` - Complete project documentation
- `QUICK_START.md` - 5-minute setup guide
- `SETUP.md` - Detailed installation instructions
- `DEPLOYMENT.md` - Multi-platform deployment guide
- `CONTRIBUTING.md` - Contribution guidelines
- `TESTING_CHECKLIST.md` - 400+ verification items
- `PROJECT_SUMMARY.md` - Complete overview

#### Testing
- 100+ unit tests for validators
- Test coverage for all validation functions
- Edge case testing
- pytest configuration

#### Deployment Ready
- Environment variable configuration
- `.env.example` template
- Docker support preparation
- Render.com deployment guide
- VPS deployment guide
- systemd service template

#### Project Structure
- Modular architecture
- Separation of concerns
- Clean handler organization
- Utility modules (validators, formatters)
- Service layer (reminders)
- Database layer (models, CRUD)

#### Technologies
- Python 3.11+
- aiogram 3.4.1
- aiosqlite 0.19.0
- APScheduler 3.10.4
- python-dotenv 1.0.0
- pytest 7.4.3

---

## Release Notes

### v1.1.0 - Button Interface
**Release Date:** December 10, 2024

**What's New:**
This release makes StudyBuddy incredibly easy to use with a new button interface! No more memorizing commands - just tap the buttons at the bottom of your chat.

**Highlights:**
- 🎮 4 persistent buttons always visible
- 📱 Perfect for mobile users
- 🆕 Beginner-friendly interface
- ⚡ One-tap access to all features
- 🔄 Commands still work if you prefer

**Breaking Changes:** None - fully backward compatible

**Migration:** Just update and restart - no configuration needed!

---

### v1.0.0 - Initial MVP
**Release Date:** December 10, 2024

**What's Included:**
Complete implementation of StudyBuddy MVP following the PRD specification.

**Core Functionality:**
- Task management (add, list, delete)
- Automated 24h reminders
- SQLite database
- Comprehensive validation
- Full documentation

**Ready for:**
- Development use
- Testing and feedback
- Production deployment
- User onboarding

---

## Upgrade Guide

### Upgrading to v1.1.0 from v1.0.0

**No breaking changes!** This is a feature addition.

1. Pull latest code:
   ```bash
   git pull origin main
   ```

2. No new dependencies - existing ones work fine

3. Restart bot:
   ```bash
   python main.py
   ```

4. Test the new buttons:
   - Send `/start` to your bot
   - You'll see the new button menu
   - Try tapping the buttons!

**That's it!** Your users will automatically see the new interface.

---

## Future Roadmap

### v1.2.0 (Planned)
- Edit existing tasks
- Task categories by subject
- Custom reminder times (48h, 1 week)
- Mark tasks complete without deleting

### v1.3.0 (Planned)
- Recurring tasks (weekly quizzes)
- Study streak tracking
- Task priority levels
- Bulk operations

### v2.0.0 (Vision)
- AI-powered study planning
- Google Calendar integration
- Collaborative group features
- Web dashboard
- Note-taking and flashcards
- Export to PDF/CSV

---

## Contributors

- Initial development and MVP implementation
- Button interface design and implementation
- Documentation and guides

---

## Feedback & Issues

Found a bug? Have a suggestion?
- Open an issue on GitHub
- Check existing issues first
- Include version number
- Provide steps to reproduce

---

**Made with ❤️ for students everywhere** 📚✨