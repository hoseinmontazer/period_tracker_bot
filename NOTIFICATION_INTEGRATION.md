# 🔔 Telegram Bot Notification System Integration

## Overview
This document explains how the notification system has been integrated into your Telegram bot for the Period Tracker application.

---

## 📁 Files Created

### 1. `modules/notifications/api.py`
Contains all API functions for interacting with the notification endpoints:
- `get_notifications()` - Fetch all notifications
- `get_unread_notifications()` - Fetch unread notifications only
- `mark_notification_read()` - Mark specific notification as read
- `mark_all_notifications_read()` - Mark all as read
- `clear_old_notifications()` - Delete old read notifications
- `get_notification_preferences()` - Get user's notification settings
- `update_notification_preferences()` - Update notification settings
- `generate_notifications()` - Trigger notification generation

### 2. `modules/notifications/handlers.py`
Telegram bot handlers for notification features:
- `show_notifications()` - Display all notifications
- `show_unread_notifications()` - Display unread notifications
- `show_notification_settings()` - Display and manage notification preferences
- `handle_notification_callback()` - Handle inline button callbacks
- `handle_preference_toggle()` - Toggle notification preferences

### 3. `modules/notifications/scheduler.py`
Automated notification delivery system:
- `send_notifications_callback()` - Scheduled job to check and send notifications
- `send_single_notification()` - Send individual notification to user
- `check_and_send_immediate_notifications()` - Check for immediate notifications after user actions

### 4. `utils/helpers.py` (Updated)
Added formatting functions:
- `format_notification_list()` - Format notification list for display
- `format_notification_preferences()` - Format preferences for display

---

## 🎯 Features Implemented

### 1. **View Notifications**
Users can view their notifications in two ways:
- **Command**: `/notifications` - Shows unread notifications
- **Dashboard Button**: "🔔 Notifications" button on main dashboard

### 2. **Notification Settings**
Users can manage their notification preferences:
- **Command**: `/notif_settings`
- **Settings Menu**: "🔔 Notification Settings" in Settings menu
- **Toggle Options**:
  - Period alerts
  - Ovulation alerts
  - Partner alerts

### 3. **Automated Delivery**
Notifications are automatically sent to users:
- **Schedule**: Every 2 hours
- **Smart Delivery**: Only sends unread notifications
- **Interactive**: Users can mark as read or view all from notification message

### 4. **Notification Types Supported**
All notification types from your API are supported:
- 🔴 Period Coming
- 🩸 Period Started
- ⚠️ Period Late
- 🌸 Ovulation Coming
- 💐 Fertile Window
- 😔 PMS Phase
- 📝 Symptom Reminder
- 💪 Wellness Reminder
- 💑 Partner's Period
- 🤝 Partner's PMS

---

## 🚀 How It Works

### User Flow

1. **User logs in** → Bot stores their token
2. **API generates notifications** → Based on cycle data and preferences
3. **Bot checks for notifications** → Every 2 hours automatically
4. **User receives notification** → With interactive buttons
5. **User can**:
   - Mark as read
   - View all notifications
   - Adjust settings

### Notification Delivery Flow

```
┌─────────────────────────────────────────────────────────┐
│  Scheduled Job (Every 2 hours)                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Check API for unread notifications                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Send notification to user with buttons                 │
│  [✅ Mark as Read] [📋 View All]                        │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  User interacts → Update API → Refresh view             │
└─────────────────────────────────────────────────────────┘
```

---

## 📱 User Commands

| Command | Description |
|---------|-------------|
| `/notifications` | View unread notifications |
| `/notif_settings` | Manage notification preferences |

---

## ⚙️ Configuration

### Notification Check Interval
In `bot.py`, the notification check runs every 2 hours:

```python
job_queue.run_repeating(
    send_notifications_callback,
    interval=7200,  # 2 hours in seconds
    first=10  # Start 10 seconds after bot starts
)
```

**To change the interval:**
- Every hour: `interval=3600`
- Every 30 minutes: `interval=1800`
- Every 4 hours: `interval=14400`

### Notification Display Limit
By default, shows max 10 notifications at once. To change:

In `utils/helpers.py`, line in `format_notification_list()`:
```python
for i, notif in enumerate(notifications[:10], 1):  # Change 10 to desired number
```

---

## 🔧 Integration Points

### 1. Dashboard Integration
The main dashboard now includes a notifications button:

```python
keyboard = [
    ["📅 Track Period", "📊 Cycle Analysis"],
    ["🔔 Notifications", "👥 Partner"],  # ← New button
    ["⚙️ Setting", "📋 Period History"]
]
```

### 2. Settings Integration
Settings menu includes notification preferences:

```python
keyboard = [
    ["✍️ Edit Profile","👤 My Profile"],
    ["🔔 Notification Settings"],  # ← New option
    ["🚪 Logout"], 
    ["⬅️ Back to Dashboard"]
]
```

### 3. Callback Handlers
Added callback handler for notification interactions:

```python
application.add_handler(
    CallbackQueryHandler(handle_notification_callback, pattern=r"^notif_")
)
```

---

## 💡 Usage Examples

### Example 1: User Receives Period Reminder

```
🔴 Period Coming Soon

Your period is expected in 3 days. Prepare supplies and plan accordingly.

📅 Scheduled: October 23, 2025 at 09:00 AM

[✅ Mark as Read] [📋 View All]
```

### Example 2: Partner Notification (Male User)

```
💑 Partner's Period Coming

Sarah's period starts tomorrow. Be extra supportive and understanding.

📅 Scheduled: October 22, 2025 at 09:00 AM

[✅ Mark as Read] [📋 View All]
```

### Example 3: Notification Settings View

```
⚙️ Notification Settings

Period Notifications:
• Period Coming: ✅
• Period Late: ✅
• Reminder Days: 3 days before

Cycle Notifications:
• Ovulation: ✅
• Fertile Window: ✅
• PMS Phase: ✅

Reminders:
• Symptom Logging: ✅
• Wellness Check-in: ✅

Partner Notifications:
• Partner's Period: ✅
• Partner's PMS: ✅

Preferred Time: 09:00:00

[✅ Period Alerts] [✅ Ovulation Alerts] [✅ Partner Alerts]
[⚙️ Advanced Settings] [⬅️ Back]
```

---

## 🔄 Triggering Notification Generation

### Automatic Generation
The API should automatically generate notifications when:
- User logs a new period
- User updates preferences
- Daily cron job runs

### Manual Generation
You can also trigger generation manually from the bot:

```python
from modules.notifications.api import generate_notifications

# In any handler
response = await generate_notifications(token)
if response.get("status") == "success":
    await update.message.reply_text(
        f"✅ Generated {len(response.get('notifications_created', []))} notifications"
    )
```

---

## 🎨 Customization

### Change Notification Emojis
In `modules/notifications/scheduler.py`:

```python
NOTIFICATION_EMOJIS = {
    "PERIOD_COMING": "🔴",  # Change to your preferred emoji
    "PERIOD_STARTED": "🩸",
    # ... etc
}
```

### Customize Notification Messages
The messages come from your API, but you can add prefixes/suffixes in `send_single_notification()`:

```python
text = f"{emoji} *{title}*\n\n{message}"
# Add custom footer:
text += "\n\n💡 Tip: Stay hydrated and rest well!"
```

---

## 🐛 Troubleshooting

### Notifications Not Sending?

1. **Check if user is registered in bot_data:**
   ```python
   users = context.application.bot_data.get("users", set())
   print(f"Registered users: {users}")
   ```

2. **Check if token exists:**
   ```python
   from utils.token_store import get_token
   token = get_token(chat_id)
   print(f"Token for {chat_id}: {token}")
   ```

3. **Check API response:**
   ```python
   response = await get_unread_notifications(token)
   print(f"API response: {response}")
   ```

4. **Check scheduler is running:**
   ```bash
   # Look for this in logs:
   "Scheduled notification checks every 2 hours"
   ```

### Buttons Not Working?

Make sure callback handler is registered:
```python
application.add_handler(
    CallbackQueryHandler(handle_notification_callback, pattern=r"^notif_")
)
```

### Wrong Notification Time?

Users need to update their preferences via API:
```python
preferences = {
    "preferred_notification_time": "08:00:00"  # 8 AM
}
await update_notification_preferences(token, preferences)
```

---

## 📊 Testing

### Test Notification Delivery
```python
# Add this command for testing
@application.command_handler('test_notif')
async def test_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    token = get_token(chat_id)
    
    # Trigger immediate check
    from modules.notifications.scheduler import check_and_send_immediate_notifications
    await check_and_send_immediate_notifications(context, chat_id, token)
    
    await update.message.reply_text("✅ Checked for notifications!")
```

### Test Notification Generation
```python
@application.command_handler('gen_notif')
async def generate_test_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    token = get_token(chat_id)
    
    response = await generate_notifications(token)
    await update.message.reply_text(f"Response: {response}")
```

---

## 🚀 Next Steps

### Recommended Enhancements

1. **Badge Count**: Show unread count on notifications button
   ```python
   unread_count = await get_unread_count(token)
   button_text = f"🔔 Notifications ({unread_count})"
   ```

2. **Notification History**: Add command to view all past notifications

3. **Snooze Feature**: Allow users to snooze notifications

4. **Custom Notification Time**: Let users set preferred time via bot

5. **Notification Categories**: Filter by type (period, partner, wellness)

---

## 📝 Summary

The notification system is now fully integrated into your Telegram bot with:

✅ Automated notification delivery every 2 hours
✅ Interactive notification messages with buttons
✅ Notification settings management
✅ Support for all notification types
✅ Dashboard and settings menu integration
✅ Proper error handling and logging

Users can now receive timely notifications about their cycle, partner's cycle, and wellness reminders directly in Telegram!
