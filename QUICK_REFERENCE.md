# 🔔 Notification System - Quick Reference Card

## 📱 User Commands
```
/notifications      → View unread notifications
/notif_settings    → Manage preferences
```

## 🎮 Dashboard Buttons
```
🔔 Notifications           → View notifications
⚙️ Settings → 🔔 Settings  → Manage preferences
```

## 🔧 Configuration Files
```
modules/notifications/api.py        → API functions
modules/notifications/handlers.py   → Bot handlers
modules/notifications/scheduler.py  → Automated delivery
utils/helpers.py                    → Formatting functions
bot.py                              → Main integration
```

## ⏰ Scheduler Settings
```python
# In bot.py, line ~150
interval=7200  # 2 hours (change as needed)
```

## 📊 Notification Types
```
🔴 PERIOD_COMING      → Period in X days
🩸 PERIOD_STARTED     → Period started
⚠️ PERIOD_LATE        → Period overdue
🌸 OVULATION_COMING   → Ovulation window
💐 FERTILE_WINDOW     → Fertile window
😔 PMS_PHASE          → PMS starting
📝 SYMPTOM_REMINDER   → Log symptoms
💪 WELLNESS_REMINDER  → Daily check-in
💑 PARTNER_PERIOD     → Partner's period
🤝 PARTNER_PMS        → Partner's PMS
```

## 🔌 API Endpoints
```
GET    /api/notifications/
GET    /api/notifications/unread/
POST   /api/notifications/{id}/mark_read/
POST   /api/notifications/mark_all_read/
DELETE /api/notifications/clear_old/
GET    /api/notification-preferences/
PUT    /api/notification-preferences/
POST   /api/generate-notifications/
```

## 🧪 Testing
```bash
# Test formatting only
python test_notifications.py

# Test with API
python test_notifications.py YOUR_TOKEN

# Test in bot
/notifications
/notif_settings
```

## 🐛 Debugging
```python
# Check users
users = context.application.bot_data.get("users", set())

# Check token
token = get_token(chat_id)

# Check API
response = await get_unread_notifications(token)

# Check logs
tail -f bot.log
```

## 📝 Common Tasks

### Add New Notification Type
1. Add emoji to `scheduler.py`
2. Update type list in docs
3. Test with sample notification

### Change Scheduler Interval
```python
# bot.py
interval=3600  # 1 hour
interval=7200  # 2 hours (default)
interval=14400 # 4 hours
```

### Change Display Limit
```python
# utils/helpers.py
for i, notif in enumerate(notifications[:10], 1):
#                                          ^^^ change this
```

### Toggle Preference
```python
preferences = {
    "period_started_alert": True,
    "ovulation_alert": False
}
await update_notification_preferences(token, preferences)
```

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| No notifications | Check login, cycle data, preferences |
| Buttons not working | Verify callback handler registered |
| Wrong time | Update preferred_notification_time |
| Too many notifications | Disable types in settings |
| Not sending | Check scheduler logs, user registration |

## 📚 Documentation Files
```
NOTIFICATION_INTEGRATION.md   → Technical guide
NOTIFICATION_SETUP.md         → Setup instructions
NOTIFICATION_USER_GUIDE.md    → User manual
NOTIFICATION_CHECKLIST.md     → Launch checklist
NOTIFICATION_FLOW.md          → Flow diagrams
NOTIFICATION_SUMMARY.md       → Implementation summary
QUICK_REFERENCE.md            → This file
```

## ✅ Pre-Launch Checklist
- [ ] Bot starts without errors
- [ ] Commands work
- [ ] Scheduler runs
- [ ] API responds
- [ ] Buttons work
- [ ] Preferences save
- [ ] Notifications send
- [ ] Documentation complete

## 🚀 Launch Steps
1. Test with small group
2. Monitor for 24 hours
3. Gather feedback
4. Fix issues
5. Full rollout

## 📞 Quick Help
```
Logs:     tail -f bot.log
Status:   ps aux | grep bot.py
Restart:  pkill -f bot.py && python bot.py
Test:     python test_notifications.py
```

---

**Keep this card handy for quick reference!** 📌
