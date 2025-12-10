# Contributing to StudyBuddy Telegram Bot

First off, thank you for considering contributing to StudyBuddy! 🎉

It's people like you that make StudyBuddy such a great tool for students everywhere.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Guidelines](#coding-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code:

- Be respectful and inclusive
- Be patient and welcoming
- Be collaborative
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**To report a bug:**
1. Use the GitHub issue tracker
2. Use a clear, descriptive title
3. Describe the exact steps to reproduce
4. Provide specific examples
5. Describe the behavior you observed and expected
6. Include screenshots if applicable
7. Include your environment details (OS, Python version, etc.)

### Suggesting Features

Feature suggestions are welcome! Please:

1. Check if the feature has already been suggested
2. Provide a clear description of the feature
3. Explain why this feature would be useful
4. Include examples of how it would work

### Code Contributions

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 💻 Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- A Telegram bot token (for testing)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/your-username/studybuddy-bot.git
cd studybuddy-bot

# Add upstream remote
git remote add upstream https://github.com/original-owner/studybuddy-bot.git

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black flake8 pytest pytest-asyncio pytest-cov

# Configure environment
cp .env.example .env
# Edit .env with your test bot token

# Run tests
pytest
```

### Running the Bot Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Run bot
python main.py
```

## 📁 Project Structure

```
StudyBuddy/
├── database/          # Database layer
│   ├── db.py         # Connection management
│   └── models.py     # CRUD operations
├── handlers/         # Command handlers
│   ├── start.py      # /start command
│   ├── add.py        # /add command
│   ├── list.py       # /list command
│   ├── delete.py     # /delete command
│   └── help.py       # /help command
├── services/         # Background services
│   └── reminder.py   # Reminder scheduler
├── utils/           # Utility functions
│   ├── validators.py # Input validation
│   └── formatters.py # Message formatting
├── keyboards/       # Telegram keyboards
│   └── reply.py     # Inline keyboards
├── states/          # FSM states
│   └── task_states.py
├── tests/          # Test files
└── main.py         # Entry point
```

## 📝 Coding Guidelines

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: Max 88 characters (Black default)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Organized in three groups (standard, third-party, local)

### Code Formatting

Use `black` for automatic formatting:

```bash
# Format all files
black .

# Check without modifying
black --check .
```

### Linting

Use `flake8` for linting:

```bash
flake8 . --max-line-length=88 --extend-ignore=E203
```

### Type Hints

Use type hints where appropriate:

```python
from typing import Optional, List, Dict, Any

async def get_user_tasks(user_id: int) -> List[Dict[str, Any]]:
    """Get all tasks for a user."""
    pass
```

### Documentation

- **Docstrings**: Use for all functions, classes, and modules
- **Comments**: Explain "why", not "what"
- **README updates**: Update documentation for new features

**Docstring format:**

```python
def validate_date(date_string: str) -> tuple[bool, Optional[date], Optional[str]]:
    """
    Validate and parse a date string.

    Args:
        date_string: Date string to validate.

    Returns:
        Tuple of (is_valid, parsed_date, error_message)
        
    Examples:
        >>> validate_date("25/12/2025")
        (True, date(2025, 12, 25), None)
    """
    pass
```

## 🧪 Testing Guidelines

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Test both success and failure cases
- Aim for >85% code coverage

**Test structure:**

```python
import pytest
from utils.validators import validate_date

class TestValidateDate:
    """Test cases for date validation."""
    
    def test_valid_date_slash_format(self):
        """Test valid date with slash format."""
        is_valid, parsed_date, error = validate_date("25/12/2025")
        assert is_valid is True
        assert parsed_date is not None
        assert error is None
    
    def test_invalid_date_format(self):
        """Test invalid date format."""
        is_valid, parsed_date, error = validate_date("invalid")
        assert is_valid is False
        assert error is not None
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_validators.py

# Run specific test
pytest tests/test_validators.py::TestValidateDate::test_valid_date
```

### Test Coverage

Maintain minimum 85% code coverage:

```bash
pytest --cov=. --cov-report=term-missing
```

## 📝 Commit Guidelines

### Commit Message Format

Use conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```bash
feat(handlers): add /edit command for updating tasks

Added new handler to allow users to edit existing tasks.
Includes validation and confirmation flow.

Closes #42

---

fix(reminder): correct timezone handling

Fixed bug where reminders were sent at wrong time due to
timezone conversion issue.

Fixes #38

---

docs(readme): update installation instructions

Clarified virtual environment setup steps for Windows users.
```

### Branch Naming

Use descriptive branch names:

```bash
feature/add-edit-command
fix/reminder-timezone-bug
docs/update-deployment-guide
refactor/database-connection
```

## 🔄 Pull Request Process

1. **Update your fork**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes**:
   - Write code
   - Add tests
   - Update documentation

4. **Test thoroughly**:
   ```bash
   pytest
   black --check .
   flake8 .
   ```

5. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**:
   - Go to GitHub
   - Click "New Pull Request"
   - Fill in the template
   - Link related issues

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests provide good coverage
```

## 🐛 Reporting Bugs

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Send command '...'
2. Enter data '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., macOS 13.0]
- Python version: [e.g., 3.11.0]
- Bot version/commit: [e.g., v1.0.0 or commit hash]

**Additional context**
Any other relevant information.
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Is your feature related to a problem?**
A clear description of the problem.

**Describe the solution**
How you'd like the feature to work.

**Describe alternatives**
Any alternative solutions you've considered.

**Additional context**
Mockups, examples, or other relevant information.
```

## 🏆 Recognition

Contributors will be:
- Listed in the README.md
- Mentioned in release notes
- Given credit in commit messages

## 📞 Questions?

- Open a GitHub discussion
- Tag maintainers in issues
- Check existing documentation

## 🎯 Good First Issues

Look for issues tagged with:
- `good first issue` - Great for newcomers
- `help wanted` - We need community help
- `documentation` - Improve docs

## 📚 Resources

- [aiogram Documentation](https://docs.aiogram.dev/)
- [Python asyncio Guide](https://docs.python.org/3/library/asyncio.html)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

---

**Thank you for contributing to StudyBuddy! 🎓📚**

Your efforts help students worldwide stay organized and succeed academically.