# 🔔 Notifications Module

## Overview
This module handles all notification-related functionality for the Period Tracker Telegram bot, including fetching, displaying, and managing user notifications.

---

## 📁 Module Structure

```
modules/notifications/
├── __init__.py          # Module initialization
├── api.py              # API communication functions
├── handlers.py         # Telegram bot handlers
├── scheduler.py        # Automated notification delivery
└── README.md          # This file
```

---

## 🔌 API Functions (`api.py`)

### Notification Management
- `get_notifications(token)` - Fetch all notifications
- `get_unread_notifications(token)` - Fetch unread notifications only
- `mark_notification_read(token, notification_id)` - Mark specific notification as read
- `mark_all_notifications_read(token)` - Mark all notifications as read
- `clear_old_notifications(token)` - Delete old read notifications

### Preferences Management
- `get_notification_preferences(token)` - Get user's notification settings
- `update_notification_preferences(token, preferences)` - Update notification settings

### Notification Generation
- `generate_notifications(token)` - Trigger notification generation based on cycle data

---

## 🎮 Bot Handlers (`handlers.py`)

### Display Handlers
- `show_notifications(update, context)` - Display all notifications
- `show_unread_notifications(update, context)` - Display unread notifications
- `show_notification_settings(update, context)` - Display notification preferences

### Action Handlers
- `handle_notification_callback(update, context)` - Handle inline button callbacks
- `handle_preference_toggle(update, context, action)` - Toggle notification preferences

---

## ⏰ Scheduler (`scheduler.py`)

### Automated Delivery
- `send_notifications_callback(context)` - Scheduled job to check and send notifications
- `send_single_notification(context, chat_id, notification, token)` - Send individual notification
- `check_and_send_immediate_notifications(context, chat_id, token)` - Check for immediate notifications

### Configuration
- Runs every 2 hours by default
- Sends only unread notifications
- Includes interactive buttons for user actions

---

## 🎯 Supported Notification Types

| Type | Emoji | Description |
|------|-------|-------------|
| PERIOD_COMING | 🔴 | Period coming soon alert |
| PERIOD_STARTED | 🩸 | Period has started |
| PERIOD_LATE | ⚠️ | Period is late |
| OVULATION_COMING | 🌸 | Ovulation window alert |
| FERTILE_WINDOW | 💐 | Fertile window starting |
| PMS_PHASE | 😔 | PMS phase starting |
| SYMPTOM_REMINDER | 📝 | Reminder to log symptoms |
| WELLNESS_REMINDER | 💪 | Reminder to log wellness |
| PARTNER_PERIOD | 💑 | Partner's period coming |
| PARTNER_PMS | 🤝 | Partner's PMS phase |

---

## 🔗 Integration Points

### Commands
```python
/notifications      # View unread notifications
/notif_settings    # Manage notification preferences
```

### Dashboard Integration
```python
keyboard = [
    ["🔔 Notifications", "👥 Partner"],
    # ...
]
```

### Settings Integration
```python
keyboard = [
    ["🔔 Notification Settings"],
    # ...
]
```

### Callback Handlers
```python
application.add_handler(
    CallbackQueryHandler(handle_notification_callback, pattern=r"^notif_")
)
```

---

## 📊 Usage Examples

### Example 1: Fetch Unread Notifications
```python
from modules.notifications.api import get_unread_notifications

response = await get_unread_notifications(token)
if response.get("status") == "success":
    notifications = response.get("data", [])
    count = response.get("count", 0)
    print(f"Found {count} unread notifications")
```

### Example 2: Mark Notification as Read
```python
from modules.notifications.api import mark_notification_read

response = await mark_notification_read(token, notification_id=123)
if response.get("status") == "success":
    print("Notification marked as read")
```

### Example 3: Update Preferences
```python
from modules.notifications.api import update_notification_preferences

preferences = {
    "period_started_alert": True,
    "ovulation_alert": False,
    "preferred_notification_time": "08:00:00"
}

response = await update_notification_preferences(token, preferences)
if response.get("status") == "success":
    print("Preferences updated")
```

### Example 4: Send Immediate Notification Check
```python
from modules.notifications.scheduler import check_and_send_immediate_notifications

# After user logs a period
await check_and_send_immediate_notifications(context, chat_id, token)
```

---

## 🔧 Configuration

### Scheduler Interval
In `bot.py`:
```python
job_queue.run_repeating(
    send_notifications_callback,
    interval=7200,  # 2 hours
    first=10
)
```

### Display Limit
In `utils/helpers.py`:
```python
for i, notif in enumerate(notifications[:10], 1):  # Max 10
```

### Emoji Mapping
In `scheduler.py`:
```python
NOTIFICATION_EMOJIS = {
    "PERIOD_COMING": "🔴",
    # ... customize as needed
}
```

---

## 🧪 Testing

### Run Tests
```bash
python test_notifications.py YOUR_AUTH_TOKEN
```

### Test Commands
Add to `bot.py` for debugging:
```python
@application.command_handler('test_notif')
async def test_notification(update, context):
    # Test notification delivery
    pass
```

---

## 🐛 Troubleshooting

### Common Issues

**Notifications not sending:**
- Check if user is in `bot_data['users']`
- Verify token exists in `user_tokens.json`
- Check API response for errors
- Verify scheduler is running

**Buttons not working:**
- Ensure callback handler is registered
- Check callback_data pattern matches

**Wrong notification time:**
- Update `preferred_notification_time` in preferences
- Regenerate notifications

---

## 📝 Dependencies

- `aiohttp` - For async API calls
- `python-telegram-bot` - For Telegram bot functionality
- `logging` - For error tracking

---

## 🚀 Future Enhancements

- [ ] Notification snooze feature
- [ ] Custom notification messages
- [ ] Notification categories/filters
- [ ] Rich notifications with images
- [ ] Notification history view
- [ ] Badge count on buttons
- [ ] Push notification support
- [ ] Email notification fallback

---

## 📚 Related Documentation

- [Integration Guide](../../NOTIFICATION_INTEGRATION.md)
- [Setup Guide](../../NOTIFICATION_SETUP.md)
- [User Guide](../../NOTIFICATION_USER_GUIDE.md)

---

## 🤝 Contributing

When adding new notification types:
1. Add emoji to `NOTIFICATION_EMOJIS` in `scheduler.py`
2. Update type list in this README
3. Test with sample notification
4. Update user documentation

---

## 📄 License

Part of the Period Tracker Telegram Bot project.
