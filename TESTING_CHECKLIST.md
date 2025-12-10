# ✅ Testing Checklist for StudyBuddy Bot

Use this checklist to verify that your StudyBuddy bot is working correctly.

## 📋 Pre-Launch Checklist

### Environment Setup
- [ ] Python 3.11+ installed (`python --version`)
- [ ] Virtual environment created (`venv/` folder exists)
- [ ] Dependencies installed (`pip list | grep aiogram`)
- [ ] `.env` file created with BOT_TOKEN
- [ ] Bot token is valid (from @BotFather)

### Database Setup
- [ ] Database initializes without errors
- [ ] `studybuddy.db` file created (or PostgreSQL connected)
- [ ] Tables created (users, tasks)
- [ ] Indexes created successfully

### Bot Startup
- [ ] Bot starts without errors
- [ ] "Bot started: @username" appears in logs
- [ ] "Starting polling..." appears in logs
- [ ] No error messages in startup sequence
- [ ] Reminder service starts successfully

---

## 🧪 Functional Testing

### 1. /start Command
- [ ] Bot responds to `/start`
- [ ] Welcome message displays correctly
- [ ] User is registered in database
- [ ] First name appears in greeting
- [ ] Quick start instructions shown

**Expected Output:**
```
👋 Welcome to StudyBuddy, [YourName]!

I help you manage assignments and exam deadlines...
```

---

### 2. /help Command
- [ ] Bot responds to `/help`
- [ ] All commands listed
- [ ] Descriptions are clear
- [ ] Tips section shown
- [ ] Contact information displayed

**Expected Output:**
```
📚 StudyBuddy Help

Available Commands:
🚀 /start - Start the bot...
```

---

### 3. /add Command (Add Task Flow)

#### Step 1: Initiate
- [ ] Command starts conversation
- [ ] Task type keyboard appears
- [ ] Both buttons work (Assignment/Exam)

#### Step 2: Task Type Selection
- [ ] Click "Assignment" works
- [ ] Click "Exam" works
- [ ] Typing "1" or "2" works
- [ ] Invalid input shows error message

#### Step 3: Task Title
- [ ] Prompt for title appears
- [ ] Valid title accepted (e.g., "Math Homework")
- [ ] Empty title rejected with error
- [ ] Title too short rejected (<3 chars)
- [ ] Title too long rejected (>200 chars)
- [ ] Multiple spaces normalized

**Test Cases:**
- [ ] Normal title: "Math Homework Chapter 5" ✅
- [ ] Empty: "" ❌
- [ ] Too short: "AB" ❌
- [ ] Too long: 201 characters ❌
- [ ] Special chars: "Physics Test #3" ✅

#### Step 4: Due Date
- [ ] Prompt for date appears
- [ ] Valid future date accepted (DD/MM/YYYY)
- [ ] Alternative format works (DD.MM.YYYY)
- [ ] Past date rejected
- [ ] Invalid format rejected
- [ ] Today's date rejected

**Test Cases:**
- [ ] Future date: "25/12/2025" ✅
- [ ] Today: [today's date] ❌
- [ ] Past: "01/01/2020" ❌
- [ ] Invalid: "32/13/2025" ❌
- [ ] Wrong format: "2025/12/25" ❌
- [ ] Text: "tomorrow" ❌

#### Confirmation
- [ ] Success message displays
- [ ] Task details shown correctly
- [ ] Due date formatted nicely
- [ ] Reminder date shown (24h before)
- [ ] Emoji icons display

**Expected Output:**
```
✅ Task Added Successfully!

📝 Math Homework Chapter 5
📅 Due: December 25, 2025
⏰ Reminder: December 24, 2025
```

---

### 4. /list Command

#### Empty State
- [ ] Shows friendly message when no tasks
- [ ] Suggests using /add

**Expected:**
```
🎉 No upcoming tasks!

Use /add to create a new task.
```

#### With Tasks
- [ ] All tasks displayed
- [ ] Sorted by due date (earliest first)
- [ ] Task numbers shown (1, 2, 3...)
- [ ] Icons show correct type (📝/📖)
- [ ] Due dates formatted nicely
- [ ] Relative time shown ("in 5 days")

**Create test tasks first, then verify:**
- [ ] Task 1: Assignment due tomorrow
- [ ] Task 2: Exam due in 5 days
- [ ] Task 3: Assignment due in 10 days
- [ ] All show in correct order

**Expected:**
```
📋 Your Upcoming Tasks:

1. 📝 Math Homework
   Due: Dec 11, 2025 (tomorrow)

2. 📖 Physics Exam
   Due: Dec 15, 2025 (in 5 days)
```

---

### 5. /delete Command

#### Empty State
- [ ] Shows message when no tasks
- [ ] Suggests using /add

#### With Tasks
- [ ] Task list displays
- [ ] Task numbers correct
- [ ] Short date format shown

#### Task Selection
- [ ] Valid number accepted (e.g., "1")
- [ ] Invalid number rejected
- [ ] Number too high rejected
- [ ] Non-number rejected

**Test Cases:**
- [ ] Valid: "1" ✅
- [ ] Invalid: "99" ❌
- [ ] Invalid: "abc" ❌
- [ ] Invalid: "0" ❌

#### Confirmation
- [ ] Confirmation prompt appears
- [ ] Task details shown
- [ ] YES/NO buttons work
- [ ] Typing "YES" works
- [ ] Typing "NO" works
- [ ] Invalid response shows error

#### Deletion
- [ ] Task deleted from database
- [ ] Success message shown
- [ ] Task no longer in /list
- [ ] Cancel preserves task

**Test Flow:**
1. [ ] Add a test task
2. [ ] Use /delete
3. [ ] Select task number
4. [ ] Confirm with YES
5. [ ] Verify task deleted
6. [ ] Check /list (task gone)

---

### 6. /cancel Command
- [ ] Works during /add flow
- [ ] Works during /delete flow
- [ ] Clears current state
- [ ] Shows confirmation message
- [ ] Can start new command after

---

### 7. Reminder System

#### Setup
- [ ] Create task due tomorrow
- [ ] Wait for reminder interval (or force check)
- [ ] Verify reminder sent

#### Reminder Content
- [ ] Reminder message received
- [ ] Task details correct
- [ ] "Tomorrow" mentioned
- [ ] Emoji icons present
- [ ] Motivational message included

**Expected:**
```
⏰ REMINDER

📝 Math Homework Chapter 5
📅 Due: Tomorrow, Monday (December 11, 2025)

Don't forget! 📚
```

#### Reminder Logic
- [ ] Reminder sent 24h before due date
- [ ] Only sent once (no duplicates)
- [ ] Not sent for past tasks
- [ ] Multiple tasks handled correctly

---

## 🔍 Edge Cases

### Input Validation
- [ ] Very long task title (190+ chars)
- [ ] Task with only spaces
- [ ] Task with special characters (!@#$%^&*)
- [ ] Dates with different separators (/, ., -)
- [ ] Leap year dates (29/02/2024)
- [ ] End of month dates (31/01/2025)

### Concurrent Users
- [ ] User A's tasks separate from User B
- [ ] Multiple users can use /add simultaneously
- [ ] Database handles concurrent writes

### State Management
- [ ] /cancel works at any step
- [ ] Starting new command clears old state
- [ ] Timeout clears state (if implemented)
- [ ] Invalid input doesn't break state

### Database
- [ ] Task IDs unique
- [ ] User IDs stored correctly
- [ ] Timestamps accurate
- [ ] Foreign keys enforced
- [ ] Indexes working (check query speed)

---

## 🐛 Error Handling

### Network Errors
- [ ] Bot handles Telegram API timeout
- [ ] Retries failed message sends
- [ ] Logs network errors

### Database Errors
- [ ] Handles database connection failure
- [ ] Handles locked database (SQLite)
- [ ] Shows user-friendly error messages
- [ ] Logs technical details

### Invalid Bot Token
- [ ] Clear error message on startup
- [ ] Doesn't crash
- [ ] Tells user to check .env

---

## 📊 Performance Testing

### Response Times
- [ ] /start responds < 2 seconds
- [ ] /list responds < 2 seconds
- [ ] /add flow steps < 2 seconds each
- [ ] Database queries < 100ms

### Load Testing
- [ ] 10 tasks in list displays quickly
- [ ] 50 tasks handled (max limit)
- [ ] Multiple rapid commands handled

---

## 🔒 Security Testing

### Input Sanitization
- [ ] SQL injection attempts fail
- [ ] Script injection attempts blocked
- [ ] Long strings don't crash bot
- [ ] Special characters handled safely

### Data Privacy
- [ ] Users only see their own tasks
- [ ] Can't delete other users' tasks
- [ ] User IDs not exposed

---

## 📝 Logging

### Log Quality
- [ ] Startup logged
- [ ] Each command logged
- [ ] Errors logged with stack traces
- [ ] User IDs in logs (for debugging)
- [ ] No sensitive data in logs

### Log Levels
- [ ] INFO for normal operations
- [ ] WARNING for recoverable issues
- [ ] ERROR for failures
- [ ] DEBUG (when enabled) is verbose

---

## 🚀 Pre-Deployment Checklist

### Code Quality
- [ ] No hardcoded secrets
- [ ] All TODOs resolved
- [ ] Comments are helpful
- [ ] No debug print statements

### Configuration
- [ ] .env.example updated
- [ ] README.md accurate
- [ ] All documentation current
- [ ] Deployment guide tested

### Testing
- [ ] All unit tests pass (`pytest`)
- [ ] Manual tests completed
- [ ] Edge cases covered
- [ ] Error scenarios tested

### Deployment
- [ ] Bot token in environment (not code)
- [ ] Database URL configured
- [ ] Log level appropriate (INFO)
- [ ] Reminder interval set correctly

---

## ✅ Final Verification

### Smoke Test Sequence
1. [ ] Start bot (`python main.py`)
2. [ ] Send `/start` - get welcome
3. [ ] Send `/help` - get commands
4. [ ] Send `/add` - create assignment
5. [ ] Send `/add` - create exam
6. [ ] Send `/list` - see both tasks
7. [ ] Send `/delete` - remove one task
8. [ ] Send `/list` - verify deletion
9. [ ] Wait for reminder (or test manually)
10. [ ] Stop bot (Ctrl+C) - clean shutdown

### Success Criteria
- [ ] All core features work
- [ ] No errors in logs
- [ ] User experience smooth
- [ ] Data persists correctly
- [ ] Reminders sent on time

---

## 🎯 Production Readiness

Before deploying to production:

- [ ] All tests passing
- [ ] Documentation complete
- [ ] Deployment guide followed
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] Error notifications set up
- [ ] Domain/bot verified
- [ ] Beta users invited
- [ ] Feedback mechanism ready

---

## 📞 If Tests Fail

1. **Check logs** - Look for error messages
2. **Verify config** - Ensure .env is correct
3. **Database** - Check studybuddy.db exists
4. **Dependencies** - Run `pip install -r requirements.txt`
5. **Python version** - Must be 3.11+
6. **Token** - Verify bot token is valid
7. **Clean slate** - Delete DB and restart

---

## 🎉 Success!

When all checkboxes are ✅:

**Your StudyBuddy bot is production-ready!** 🚀

Deploy with confidence and help students succeed! 📚✨

---

**Testing Date:** _____________  
**Tested By:** _____________  
**Bot Version:** v1.0  
**Status:** [ ] Pass  [ ] Fail

**Notes:**
_______________________________________
_______________________________________
_______________________________________