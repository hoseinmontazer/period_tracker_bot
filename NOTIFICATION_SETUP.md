# 🚀 Quick Setup Guide - Notification System

## Prerequisites
- Your Django API must have the notification endpoints implemented
- Bot must be running with job queue enabled

---

## 📦 Installation Steps

### 1. No Additional Dependencies Needed
All required libraries are already in your `requirements.txt`:
- `python-telegram-bot` (already installed)
- `aiohttp` (already installed)

### 2. Verify File Structure
Make sure these files exist:
```
modules/
├── notifications/
│   ├── __init__.py
│   ├── api.py
│   ├── handlers.py
│   └── scheduler.py
```

### 3. Test the Integration

#### Test 1: Check if bot starts
```bash
python bot.py
```

Look for this in logs:
```
Scheduled notification checks every 2 hours
```

#### Test 2: Test notification command
In Telegram, send:
```
/notifications
```

Expected response:
- If no notifications: "✅ No unread notifications!"
- If notifications exist: List of notifications with buttons

#### Test 3: Test settings command
In Telegram, send:
```
/notif_settings
```

Expected response: Notification preferences with toggle buttons

---

## 🔧 Configuration

### Adjust Notification Check Frequency

In `bot.py`, find this section:
```python
job_queue.run_repeating(
    send_notifications_callback,
    interval=7200,  # ← Change this value
    first=10
)
```

**Common intervals:**
- Every 30 minutes: `interval=1800`
- Every hour: `interval=3600`
- Every 2 hours: `interval=7200` (default)
- Every 4 hours: `interval=14400`

### Adjust Notification Display Limit

In `utils/helpers.py`, find `format_notification_list()`:
```python
for i, notif in enumerate(notifications[:10], 1):  # ← Change 10 to desired limit
```

---

## 🧪 Testing Checklist

- [ ] Bot starts without errors
- [ ] `/notifications` command works
- [ ] `/notif_settings` command works
- [ ] Dashboard shows "🔔 Notifications" button
- [ ] Settings menu shows "🔔 Notification Settings"
- [ ] Clicking notification buttons works
- [ ] Scheduled job runs (check logs after 2 hours)

---

## 📱 User Testing Flow

### Test as Female User:
1. Login to bot
2. Track a period
3. Wait for API to generate notifications (or trigger manually)
4. Check `/notifications` - should see period-related notifications
5. Click "✅ Mark as Read" - notification should be marked
6. Go to `/notif_settings` - toggle some preferences
7. Verify preferences are saved

### Test as Male User (Partner Tracking):
1. Login to bot
2. Link with a partner
3. Wait for API to generate partner notifications
4. Check `/notifications` - should see partner-related notifications
5. Verify partner alerts work

---

## 🔍 Debugging

### Enable Debug Logging

Add to `bot.py`:
```python
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # ← Change to DEBUG
)
```

### Check User Registration

Add this test command to `bot.py`:
```python
async def check_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = context.application.bot_data.get("users", set())
    await update.message.reply_text(f"Registered users: {len(users)}\n{users}")

application.add_handler(CommandHandler('check_users', check_users))
```

### Check Token Storage

Add this test command:
```python
async def check_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    token = get_token(chat_id)
    if token:
        await update.message.reply_text(f"✅ Token exists: {token[:20]}...")
    else:
        await update.message.reply_text("❌ No token found")

application.add_handler(CommandHandler('check_token', check_token))
```

### Test API Connection

Add this test command:
```python
async def test_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from modules.notifications.api import get_unread_notifications
    chat_id = update.effective_chat.id
    token = get_token(chat_id)
    
    if not token:
        await update.message.reply_text("❌ No token")
        return
    
    response = await get_unread_notifications(token)
    await update.message.reply_text(f"API Response:\n{response}")

application.add_handler(CommandHandler('test_api', test_api))
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "No token found"
**Solution:** User needs to login first
```python
# Make sure user is logged in
/start → Login → Enter credentials
```

### Issue 2: Notifications not sending automatically
**Solution:** Check if job queue is running
```python
# In bot.py, verify:
job_queue = application.job_queue
if job_queue:
    # Jobs are registered here
```

### Issue 3: API returns error
**Solution:** Check API endpoint configuration
```python
# In config.py, verify:
BASE_URL = "https://api-period.shirpala.ir/"  # Must end with /
```

### Issue 4: Buttons not responding
**Solution:** Make sure callback handler is registered
```python
# In bot.py, verify this line exists:
application.add_handler(
    CallbackQueryHandler(handle_notification_callback, pattern=r"^notif_")
)
```

### Issue 5: Scheduler not running
**Solution:** Check if bot_data has users
```python
# Users must be registered in bot_data
users = context.application.bot_data.setdefault("users", set())
users.add(chat_id)
```

---

## 📊 Monitoring

### Check Logs for These Messages:

**Successful startup:**
```
Scheduled notification checks every 2 hours
```

**Notification check running:**
```
Running send_notifications_callback
```

**Notification sent:**
```
Sent notification 123 to 456789
```

**Errors to watch for:**
```
No token for chat_id 123, skipping
Error fetching notifications for 123: ...
Failed to send notification ...
```

---

## ✅ Verification

After setup, verify everything works:

1. **Start bot**: `python bot.py`
2. **Login as user**: `/start` → Login
3. **Check notifications**: `/notifications`
4. **Check settings**: `/notif_settings`
5. **Wait 2 hours**: Check if automatic notifications arrive
6. **Check logs**: Look for scheduler messages

---

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Bot starts without errors
- ✅ Commands respond correctly
- ✅ Buttons are clickable and functional
- ✅ Notifications appear automatically
- ✅ Settings can be toggled
- ✅ Logs show scheduler running

---

## 📞 Need Help?

If you encounter issues:
1. Check the logs for error messages
2. Verify API endpoints are working
3. Test with debug commands above
4. Check that all files are in place
5. Verify bot token and API URL in config.py

---

## 🚀 Ready to Go!

Your notification system is now set up and ready to use. Users will receive:
- Period reminders
- Ovulation alerts
- Partner notifications
- Wellness reminders
- And more!

All delivered automatically to their Telegram!
