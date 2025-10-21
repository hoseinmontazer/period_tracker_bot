# 🔄 Notification System Flow Diagram

## 📊 Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DJANGO API BACKEND                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐      ┌──────────────────┐                   │
│  │  Notification    │      │  Notification    │                   │
│  │  Model           │◄─────┤  Generator       │                   │
│  │  (Database)      │      │  (Logic)         │                   │
│  └────────┬─────────┘      └────────▲─────────┘                   │
│           │                         │                              │
│           │                         │                              │
│  ┌────────▼─────────────────────────┴─────────┐                   │
│  │         API Endpoints                      │                   │
│  │  • GET /api/notifications/                 │                   │
│  │  • GET /api/notifications/unread/          │                   │
│  │  • POST /api/notifications/{id}/mark_read/ │                   │
│  │  • POST /api/notifications/mark_all_read/  │                   │
│  │  • GET /api/notification-preferences/      │                   │
│  │  • PUT /api/notification-preferences/      │                   │
│  │  • POST /api/generate-notifications/       │                   │
│  └────────────────────────────────────────────┘                   │
│                           │                                        │
└───────────────────────────┼────────────────────────────────────────┘
                            │
                            │ HTTPS/JSON
                            │
┌───────────────────────────▼────────────────────────────────────────┐
│                    TELEGRAM BOT (Python)                           │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              modules/notifications/api.py                    │ │
│  │  • get_notifications()                                       │ │
│  │  • get_unread_notifications()                                │ │
│  │  • mark_notification_read()                                  │ │
│  │  • update_notification_preferences()                         │ │
│  └────────────────────┬─────────────────────────────────────────┘ │
│                       │                                            │
│  ┌────────────────────▼─────────────────────────────────────────┐ │
│  │           modules/notifications/handlers.py                  │ │
│  │  • show_notifications()                                      │ │
│  │  • show_unread_notifications()                               │ │
│  │  • show_notification_settings()                              │ │
│  │  • handle_notification_callback()                            │ │
│  └────────────────────┬─────────────────────────────────────────┘ │
│                       │                                            │
│  ┌────────────────────▼─────────────────────────────────────────┐ │
│  │           modules/notifications/scheduler.py                 │ │
│  │  • send_notifications_callback() [Every 2 hours]             │ │
│  │  • send_single_notification()                                │ │
│  └────────────────────┬─────────────────────────────────────────┘ │
│                       │                                            │
│  ┌────────────────────▼─────────────────────────────────────────┐ │
│  │                  utils/helpers.py                            │ │
│  │  • format_notification_list()                                │ │
│  │  • format_notification_preferences()                         │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             │ Telegram Bot API
                             │
┌────────────────────────────▼───────────────────────────────────────┐
│                         TELEGRAM USER                              │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  📱 Receives Notifications:                                        │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ 🔴 Period Coming Soon                                        │ │
│  │                                                              │ │
│  │ Your period is expected in 3 days.                          │ │
│  │                                                              │ │
│  │ [✅ Mark as Read] [📋 View All]                             │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  🎮 Can Use Commands:                                              │
│  • /notifications - View unread                                   │
│  • /notif_settings - Manage preferences                           │
│                                                                    │
│  🖱️ Can Use Dashboard:                                             │
│  • 🔔 Notifications button                                        │
│  • ⚙️ Settings → 🔔 Notification Settings                        │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Notification Delivery Flow

```
START
  │
  ▼
┌─────────────────────────────────────┐
│ Scheduled Job Triggers               │
│ (Every 2 hours)                      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Load User Tokens from JSON           │
│ (data/user_tokens.json)              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Get Registered Users                 │
│ (from bot_data['users'])             │
└──────────────┬──────────────────────┘
               │
               ▼
         ┌─────┴─────┐
         │ For Each  │
         │   User    │
         └─────┬─────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Call API: get_unread_notifications() │
└──────────────┬──────────────────────┘
               │
               ▼
         ┌─────┴─────┐
         │  Has      │
    ┌────┤  Unread?  ├────┐
    │    └───────────┘    │
   NO                    YES
    │                      │
    ▼                      ▼
  Skip            ┌─────────────────┐
                  │ For Each Notif  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────────────┐
                  │ Format Notification     │
                  │ • Add emoji             │
                  │ • Format message        │
                  │ • Create buttons        │
                  └────────┬────────────────┘
                           │
                           ▼
                  ┌─────────────────────────┐
                  │ Send to User via        │
                  │ Telegram Bot API        │
                  └────────┬────────────────┘
                           │
                           ▼
                  ┌─────────────────────────┐
                  │ Log Success/Error       │
                  └─────────────────────────┘
                           │
                           ▼
                         END
```

---

## 👤 User Interaction Flow

```
USER OPENS BOT
      │
      ▼
┌──────────────────┐
│ /start           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Login            │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Dashboard                            │
│ ┌──────────────────────────────────┐ │
│ │ 📅 Track Period                  │ │
│ │ 🔔 Notifications  ◄──────────────┼─┐
│ │ ⚙️ Settings                      │ │ │
│ └──────────────────────────────────┘ │ │
└──────────────────────────────────────┘ │
                                         │
         ┌───────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Notification List                    │
│ ┌──────────────────────────────────┐ │
│ │ 1. 🔴 Period Coming Soon         │ │
│ │    Your period in 3 days...      │ │
│ │                                  │ │
│ │ 2. 🌸 Ovulation Window           │ │
│ │    You are entering...           │ │
│ │                                  │ │
│ │ [✅ Mark All Read]               │ │
│ │ [🗑️ Clear Old]                   │ │
│ │ [⬅️ Back]                        │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
         │
         ├─────────────┬─────────────┐
         │             │             │
         ▼             ▼             ▼
   Mark All Read   Clear Old      Back
         │             │             │
         ▼             ▼             ▼
   Update API    Delete Old    Dashboard
```

---

## ⚙️ Settings Management Flow

```
USER CLICKS SETTINGS
      │
      ▼
┌──────────────────────────────────────┐
│ Settings Menu                        │
│ ┌──────────────────────────────────┐ │
│ │ ✍️ Edit Profile                  │ │
│ │ 🔔 Notification Settings ◄───────┼─┐
│ │ 🚪 Logout                        │ │ │
│ └──────────────────────────────────┘ │ │
└──────────────────────────────────────┘ │
                                         │
         ┌───────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Notification Settings                │
│ ┌──────────────────────────────────┐ │
│ │ Period Notifications:            │ │
│ │ • Period Coming: ✅              │ │
│ │ • Period Late: ✅                │ │
│ │                                  │ │
│ │ Cycle Notifications:             │ │
│ │ • Ovulation: ✅                  │ │
│ │ • Fertile Window: ✅             │ │
│ │                                  │ │
│ │ [✅ Period Alerts]               │ │
│ │ [✅ Ovulation Alerts]            │ │
│ │ [✅ Partner Alerts]              │ │
│ │ [⚙️ Advanced Settings]           │ │
│ │ [⬅️ Back]                        │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
         │
         ▼
   User Clicks Toggle
         │
         ▼
┌──────────────────────────────────────┐
│ 1. Get Current Preferences from API  │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ 2. Toggle Selected Preference        │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ 3. Update Preferences via API        │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ 4. Show Success Message              │
│    "✅ Notification enabled!"         │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ 5. Refresh Settings View             │
└──────────────────────────────────────┘
```

---

## 🔔 Notification Generation Flow

```
TRIGGER EVENT
(User logs period, Daily cron, Manual trigger)
      │
      ▼
┌──────────────────────────────────────┐
│ API: generate_notifications()        │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Analyze User's Cycle Data            │
│ • Last period date                   │
│ • Average cycle length               │
│ • Cycle regularity                   │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Check Notification Preferences       │
│ • Which alerts are enabled?          │
│ • Preferred notification time        │
│ • Days before period reminder        │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Calculate Upcoming Events            │
│ • Next period date                   │
│ • Ovulation date                     │
│ • Fertile window                     │
│ • PMS phase start                    │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Generate Notifications               │
│ • PERIOD_COMING (3 days before)      │
│ • OVULATION_COMING (day 14)          │
│ • FERTILE_WINDOW (day 11-13)         │
│ • PMS_PHASE (4 days before)          │
│ • WELLNESS_REMINDER (daily)          │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Check for Duplicates                 │
│ (Don't create if already exists)     │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Save to Database                     │
│ • scheduled_time                     │
│ • is_sent = False                    │
│ • is_read = False                    │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Return Success Response              │
│ {                                    │
│   "status": "success",               │
│   "message": "Generated 5 notifs",   │
│   "notifications_created": [...]     │
│ }                                    │
└──────────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

```
┌─────────────┐
│   USER      │
└──────┬──────┘
       │
       │ 1. Logs Period
       │
       ▼
┌─────────────────┐
│  DJANGO API     │
│  • Saves period │
│  • Generates    │
│    notifications│
└──────┬──────────┘
       │
       │ 2. Stores in DB
       │
       ▼
┌─────────────────┐
│  DATABASE       │
│  • Notifications│
│  • Preferences  │
└──────┬──────────┘
       │
       │ 3. Scheduled Check
       │
       ▼
┌─────────────────┐
│  TELEGRAM BOT   │
│  • Fetches      │
│    unread       │
└──────┬──────────┘
       │
       │ 4. Sends Message
       │
       ▼
┌─────────────────┐
│  USER           │
│  • Receives     │
│    notification │
└──────┬──────────┘
       │
       │ 5. Marks as Read
       │
       ▼
┌─────────────────┐
│  TELEGRAM BOT   │
│  • Calls API    │
└──────┬──────────┘
       │
       │ 6. Updates DB
       │
       ▼
┌─────────────────┐
│  DATABASE       │
│  • is_read=True │
└─────────────────┘
```

---

## 🎯 Key Integration Points

### 1. User Registration
```
User /start → Login → Token stored → Added to bot_data['users']
```

### 2. Notification Check
```
Scheduler → Load tokens → For each user → Fetch unread → Send
```

### 3. User Interaction
```
User clicks button → Callback handler → API call → Update → Refresh view
```

### 4. Preference Update
```
User toggles → Get current → Toggle value → Update API → Show success
```

---

## 📝 Summary

This notification system provides:
- ✅ Automated delivery every 2 hours
- ✅ Real-time user interactions
- ✅ Preference management
- ✅ Multiple notification types
- ✅ Clean separation of concerns
- ✅ Error handling at each step
- ✅ Scalable architecture

The flow ensures users receive timely, relevant notifications while maintaining full control over their preferences.
