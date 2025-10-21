# 🚀 Get Started with Notifications - 5 Minutes

## Step 1: Verify Files (30 seconds)
```bash
# Check if notification files exist
ls modules/notifications/
# Should see: __init__.py, api.py, handlers.py, scheduler.py
```

## Step 2: Start the Bot (1 minute)
```bash
python bot.py
```

**Look for this in the output:**
```
Scheduled notification checks every 2 hours
🤖 Period Tracker Bot is running...
```

✅ If you see this, the notification system is loaded!

## Step 3: Test as a User (2 minutes)

### In Telegram:
1. Open your bot
2. Send `/start`
3. Login with your credentials
4. You should see the dashboard with a **🔔 Notifications** button

### Test Commands:
```
/notifications      → Should show "No unread notifications" or list
/notif_settings    → Should show your notification preferences
```

## Step 4: Verify Integration (1 minute)

### Check Dashboard:
- [ ] Dashboard has "🔔 Notifications" button
- [ ] Clicking it shows notification list or "No notifications"

### Check Settings:
- [ ] Settings menu has "🔔 Notification Settings"
- [ ] Clicking it shows preferences with toggle buttons

### Check Commands:
- [ ] `/notifications` works
- [ ] `/notif_settings` works

## Step 5: Wait for Automatic Delivery (Optional)

The bot will automatically check for notifications every 2 hours. To test immediately:

1. Track a period in the bot
2. Wait a few minutes for API to generate notifications
3. Check `/notifications` again
4. You should see new notifications!

---

## ✅ Success Indicators

You're all set if:
- ✅ Bot starts without errors
- ✅ Dashboard shows notification button
- ✅ Commands respond correctly
- ✅ Settings are accessible
- ✅ No error messages in logs

---

## 🐛 Quick Troubleshooting

### "Please login first"
→ Login to the bot first: `/start` → Login

### "No notifications"
→ Normal! Track a period first, then wait for API to generate notifications

### Buttons not working
→ Make sure you're using latest Telegram version

### Bot won't start
→ Check for syntax errors: `python -m py_compile bot.py`

---

## 📚 Next Steps

Once everything works:

1. **Read User Guide**: `NOTIFICATION_USER_GUIDE.md`
2. **Customize Settings**: Adjust scheduler interval if needed
3. **Monitor Logs**: Watch for any errors
4. **Test with Real Users**: Get feedback
5. **Iterate**: Improve based on feedback

---

## 🎉 You're Done!

Your notification system is now running! Users will receive:
- Period reminders
- Ovulation alerts
- Partner notifications
- Wellness reminders
- And more!

All automatically delivered to their Telegram! 🎊

---

## 📞 Need Help?

- **Setup Issues**: Read `NOTIFICATION_SETUP.md`
- **Technical Details**: Read `NOTIFICATION_INTEGRATION.md`
- **User Questions**: Read `NOTIFICATION_USER_GUIDE.md`
- **Quick Reference**: Read `QUICK_REFERENCE.md`

---

**Total Time**: ~5 minutes
**Difficulty**: Easy
**Status**: Ready to Go! ✅
