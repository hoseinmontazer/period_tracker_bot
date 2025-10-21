# 📱 User Guide - Telegram Bot Notifications

## 🔔 What Are Notifications?

The Period Tracker bot sends you automatic reminders and alerts about:
- Your upcoming period
- Ovulation windows
- PMS phase
- Partner's cycle (for male users)
- Wellness check-ins
- And more!

---

## 🚀 Getting Started

### Step 1: Login
```
/start
→ Login
→ Enter your credentials
```

### Step 2: Enable Notifications
Notifications are enabled by default! But you can customize them:
```
/notif_settings
```

### Step 3: Receive Notifications
The bot will automatically send you notifications based on your cycle data.

---

## 📋 Available Commands

| Command | What It Does |
|---------|--------------|
| `/notifications` | View your unread notifications |
| `/notif_settings` | Manage notification preferences |

---

## 🎯 Notification Types

### For Female Users:

#### 🔴 Period Coming Soon
"Your period is expected in 3 days. Prepare supplies and plan accordingly."
- **When**: X days before your period (default: 3 days)
- **Customize**: Change reminder days in settings

#### 🩸 Period Started
"Your period has started. Remember to log your symptoms."
- **When**: On your period start date
- **Action**: Track your period in the bot

#### ⚠️ Period Late
"Your period is late. Consider taking a test or consulting a doctor."
- **When**: When your period is overdue
- **Action**: Update your period data or consult healthcare provider

#### 🌸 Ovulation Coming
"You are entering your ovulation window. Energy levels are typically highest."
- **When**: Around day 14 of your cycle
- **Info**: Best time for conception if trying

#### 💐 Fertile Window
"Your fertile window is starting."
- **When**: 3 days before ovulation
- **Info**: Increased chance of conception

#### 😔 PMS Phase
"You may experience PMS symptoms. Practice self-care and be patient."
- **When**: 3-4 days before your period
- **Tip**: Rest, hydrate, and be kind to yourself

#### 📝 Symptom Reminder
"Don't forget to log your symptoms today."
- **When**: During your period
- **Action**: Track symptoms in the bot

#### 💪 Wellness Reminder
"Time for your daily wellness check-in!"
- **When**: Daily at your preferred time
- **Action**: Fill out wellness form

### For Male Users (Partner Tracking):

#### 💑 Partner's Period Coming
"Sarah's period starts tomorrow. Be extra supportive and understanding."
- **When**: 1 day before partner's period
- **Tip**: Offer help, be patient

#### 🤝 Partner's PMS Phase
"Sarah may be experiencing PMS symptoms. Be patient and offer support."
- **When**: 3 days before partner's period
- **Tip**: Extra understanding goes a long way

---

## ⚙️ Managing Notifications

### View Notifications

**Option 1: Command**
```
/notifications
```

**Option 2: Dashboard**
```
Main Menu → 🔔 Notifications
```

### Manage Settings

**Option 1: Command**
```
/notif_settings
```

**Option 2: Settings Menu**
```
Main Menu → ⚙️ Settings → 🔔 Notification Settings
```

### Quick Toggles

In notification settings, you can quickly toggle:
- ✅/❌ Period Alerts
- ✅/❌ Ovulation Alerts
- ✅/❌ Partner Alerts

Just tap the button to enable/disable!

---

## 🎨 Notification Actions

When you receive a notification, you can:

### ✅ Mark as Read
Marks the notification as read so it won't appear in unread list.

### 📋 View All
Opens your full notification list to see all notifications.

### From Notification List:
- **✅ Mark All Read**: Marks all notifications as read
- **🗑️ Clear Old**: Deletes old read notifications (30+ days)

---

## 🔧 Customization Options

### Change Notification Time
Set when you want to receive daily notifications:
- Default: 9:00 AM
- Customize via web interface or API

### Change Period Reminder Days
Set how many days before your period you want to be reminded:
- Default: 3 days
- Options: 1-7 days
- Customize in settings

### Enable/Disable Specific Alerts
Turn on/off individual notification types:
- Period alerts
- Ovulation alerts
- PMS alerts
- Symptom reminders
- Wellness reminders
- Partner alerts

---

## 💡 Tips & Best Practices

### 1. Keep Your Cycle Data Updated
Notifications are based on your cycle data. The more accurate your data, the better your notifications!

### 2. Adjust Reminder Days
If 3 days isn't enough notice, increase it to 5 or 7 days.

### 3. Don't Miss Wellness Check-ins
Daily wellness tracking helps the bot give you better insights.

### 4. Enable Partner Notifications
If you're tracking your partner's cycle, enable partner notifications to be more supportive.

### 5. Clear Old Notifications
Regularly clear old notifications to keep your list clean.

---

## 📊 Notification Frequency

| Type | Frequency |
|------|-----------|
| Period Coming | Once per cycle |
| Period Started | Once per period |
| Period Late | Once when overdue |
| Ovulation | Once per cycle |
| Fertile Window | Once per cycle |
| PMS Phase | Once per cycle |
| Symptom Reminder | During period |
| Wellness Reminder | Daily |
| Partner Alerts | Per partner's cycle |

---

## 🔐 Privacy & Security

- ✅ Notifications are private and only visible to you
- ✅ No sensitive health data in notification titles
- ✅ Partner notifications require explicit linking
- ✅ You control all notification preferences
- ✅ Old notifications auto-delete after 30 days

---

## ❓ FAQ

### Q: I'm not receiving notifications. Why?
**A:** Check these:
1. Are you logged in? (`/start` → Login)
2. Do you have cycle data? (Track at least one period)
3. Are notifications enabled in settings? (`/notif_settings`)
4. Is your preferred time set correctly?

### Q: Can I change the notification time?
**A:** Yes! Update your preferred notification time in settings. Default is 9:00 AM.

### Q: How do I stop receiving certain notifications?
**A:** Go to `/notif_settings` and toggle off the notification types you don't want.

### Q: What happens to old notifications?
**A:** Read notifications older than 30 days are automatically deleted. You can also manually clear them.

### Q: Can I get notifications for my partner's cycle?
**A:** Yes! If you're a male user with a linked partner, enable partner notifications in settings.

### Q: How accurate are the predictions?
**A:** Predictions are based on your cycle history. The more periods you track, the more accurate they become.

### Q: Can I snooze notifications?
**A:** Not yet, but this feature is coming soon!

### Q: Do notifications work if the bot is offline?
**A:** Notifications are generated by the API and delivered when the bot is online. If the bot is offline, you'll receive them when it comes back online.

---

## 🆘 Troubleshooting

### Problem: "Please login first"
**Solution:** Login to the bot first
```
/start → Login → Enter credentials
```

### Problem: "No unread notifications"
**Solution:** Either you have no notifications, or they haven't been generated yet. Try:
```
Track a period → Wait a few minutes → Check /notifications
```

### Problem: Buttons not working
**Solution:** Make sure you're using the latest version of Telegram

### Problem: Wrong notification time
**Solution:** Update your preferred time in settings

### Problem: Too many notifications
**Solution:** Disable specific types in `/notif_settings`

---

## 📞 Support

Need help? Contact support or check the documentation:
- Bot commands: `/help`
- Settings: `/notif_settings`
- View notifications: `/notifications`

---

## 🎉 Enjoy Your Notifications!

Stay informed about your cycle with automatic, personalized notifications delivered right to your Telegram! 💜
