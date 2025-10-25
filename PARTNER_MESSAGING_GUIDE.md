# 💬 Partner Messaging System - Complete Guide

## Overview
A complete partner messaging system integrated into your Telegram Period Tracker bot, allowing partners to communicate directly through the bot.

---

## 🎯 Features Implemented

### 1. **Send Messages to Partner**
- Send text messages to your linked partner
- Real-time message delivery
- Message confirmation

### 2. **View Conversations**
- See full conversation history
- Last 15 messages displayed
- Automatic read receipts
- Timestamps for each message

### 3. **Unread Message Notifications**
- Automatic notifications for new messages
- Unread count badge
- Message preview in notifications

### 4. **Message Management**
- View all messages (sent and received)
- Mark messages as read automatically
- Message history

---

## 📱 User Commands

```bash
/messages           # Open partner messages menu
```

### Dashboard Access
```
Partner Menu → 💬 Send Message to Partner
Dashboard → 💬 Partner Messages (if added to dashboard)
```

---

## 🎮 How to Use

### Sending a Message

1. **Open Messages Menu**
   ```
   /messages
   or
   Partner Menu → 💬 Send Message to Partner
   ```

2. **Click "✉️ Send Message"**

3. **Type Your Message**
   - Type any text message
   - Click "❌ Cancel" to cancel

4. **Message Sent!**
   - You'll see a confirmation
   - Partner will receive notification

### Viewing Conversation

1. **Open Messages Menu**
   ```
   /messages
   ```

2. **Click "💬 View Conversation"**
   - Shows last 15 messages
   - Displays sender names
   - Shows timestamps
   - Automatically marks messages as read

3. **Refresh Conversation**
   - Click "🔄 Refresh" to update

### Checking Unread Messages

1. **Open Messages Menu**
   ```
   /messages
   ```

2. **See Unread Count**
   - Shows in menu: "💬 View Conversation (3 unread)"
   - Displays unread message count

3. **Automatic Notifications**
   - Bot sends notifications every 2 hours
   - Shows message preview
   - Quick action buttons

---

## 🔔 Notification System

### Automatic Message Notifications

When your partner sends a message, you'll receive:

```
💬 New Message from Sarah

Hey, how are you feeling today?...

You have 2 unread messages

[💬 View Messages] [✉️ Reply]
```

### Notification Features
- **Message Preview**: First 50 characters
- **Sender Name**: Who sent the message
- **Unread Count**: Total unread messages
- **Quick Actions**: View or reply instantly

---

## 📊 Message Display Formats

### Conversation View
```
💬 Conversation with Sarah
Total messages: 25

──────────────────────────────

🙋 You (02:30 PM):
How are you feeling today?

👤 Sarah (02:35 PM):
I'm doing well, thanks for asking!

🙋 You (02:40 PM):
That's great to hear!

Showing last 15 of 25 messages
```

### All Messages View
```
📬 All Messages

1. ✅ John → Sarah
   How are you feeling today?...
   📅 Jan 23, 02:30 PM

2. ✅ Sarah → John
   I'm doing well, thanks!...
   📅 Jan 23, 02:35 PM

3. 🆕 Sarah → John
   Don't forget to pick up groceries!
   📅 Jan 23, 03:00 PM
```

---

## 🎨 Menu Structure

### Partner Messages Menu
```
💬 Partner Messages

You have 2 unread message(s)!

Choose an option:

[💬 View Conversation (2 unread)]
[✉️ Send Message]
[📋 All Messages]
[⬅️ Back to Dashboard]
```

### Conversation Actions
```
[✉️ Send Message]
[🔄 Refresh]
[⬅️ Back]
```

---

## 🔧 API Integration

### Endpoints Used

1. **Send Message**
   ```
   POST /api/notifications/messages/
   ```

2. **Get Conversation**
   ```
   GET /api/notifications/messages/conversation/?partner_id={id}
   ```

3. **Get Unread Messages**
   ```
   GET /api/notifications/messages/unread/
   ```

4. **Get All Messages**
   ```
   GET /api/notifications/messages/
   ```

---

## 💡 Usage Examples

### Example 1: Quick Message
```
User: /messages
Bot: [Shows menu with unread count]

User: Clicks "✉️ Send Message"
Bot: "Type your message below:"

User: "Hope you're having a great day!"
Bot: "✅ Message sent to Sarah!"
```

### Example 2: Check Messages
```
User: /messages
Bot: "You have 3 unread message(s)!"

User: Clicks "💬 View Conversation"
Bot: [Shows conversation with 3 new messages]
     [Messages automatically marked as read]
```

### Example 3: Receive Notification
```
[Bot sends notification]
💬 New Message from Sarah
"Don't forget dinner tonight!"

User: Clicks "✉️ Reply"
Bot: "Type your message below:"

User: "I won't forget! See you at 7!"
Bot: "✅ Message sent!"
```

---

## 🔐 Privacy & Security

- ✅ Messages only between linked partners
- ✅ Cannot message non-partners
- ✅ Automatic authentication check
- ✅ Secure token-based API calls
- ✅ Messages stored securely on server

---

## 🎯 Best Practices

### For Users
1. **Check messages regularly** - Open /messages daily
2. **Reply promptly** - Partner will appreciate quick responses
3. **Be supportive** - Use messages to show care
4. **Keep it positive** - Encourage and support your partner

### For Developers
1. **Handle errors gracefully** - Show user-friendly messages
2. **Validate partner exists** - Check before sending
3. **Limit message length** - Consider adding character limit
4. **Rate limiting** - Prevent spam (future enhancement)

---

## 🐛 Troubleshooting

### "You don't have any partners linked yet"
**Solution:** Link a partner first
```
Partner Menu → 🤝 Add Partner → Accept Invitation
```

### "Failed to send message"
**Possible causes:**
- Partner was removed
- Network issue
- Invalid token

**Solution:**
- Check partner is still linked
- Try again
- Re-login if needed

### Messages not showing
**Solution:**
- Click "🔄 Refresh"
- Check internet connection
- Verify partner is linked

### No notification received
**Solution:**
- Wait for next check (every 2 hours)
- Check notification preferences
- Ensure bot is running

---

## 🔄 Message Flow

```
┌─────────────────────────────────────────┐
│  User Opens Messages Menu               │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  Bot Checks Unread Count                │
│  Shows menu with badge                  │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  User Clicks "Send Message"             │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  Bot Asks for Message Text              │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  User Types Message                     │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  Bot Sends to API                       │
│  API Delivers to Partner                │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  Partner Receives Notification          │
│  (Next scheduled check)                 │
└─────────────────────────────────────────┘
```

---

## 📈 Future Enhancements

- [ ] Message reactions (❤️, 👍, etc.)
- [ ] Voice messages
- [ ] Image sharing
- [ ] Message editing
- [ ] Message deletion
- [ ] Typing indicators
- [ ] Read receipts display
- [ ] Message search
- [ ] Message export
- [ ] Group messaging (multiple partners)

---

## 🎓 Tips for Partners

### For Female Users
- Share how you're feeling during different cycle phases
- Let partner know when you need support
- Communicate symptoms or discomfort
- Express appreciation for support

### For Male Users
- Check in regularly
- Offer support during difficult phases
- Ask how you can help
- Be understanding and patient
- Send encouraging messages

---

## 📊 Statistics

### Implementation
- **1** new handler file created
- **4** new API functions added
- **2** new formatting functions
- **1** new command added
- **Integrated** with existing partner system

### Features
- **Send** messages to partner
- **View** full conversation
- **Check** unread messages
- **Receive** automatic notifications
- **Reply** quickly from notifications

---

## ✅ Success Indicators

Your messaging system is working when:
- ✅ Users can send messages
- ✅ Messages appear in conversation
- ✅ Unread count is accurate
- ✅ Notifications are delivered
- ✅ Read receipts work
- ✅ No error messages

---

## 📞 Support

### For Users
- Use `/messages` command
- Check partner is linked
- Verify internet connection
- Contact support if issues persist

### For Developers
- Check API responses
- Verify token is valid
- Test with linked partners
- Review error logs

---

## 🎉 Conclusion

The partner messaging system provides a seamless way for partners to communicate and support each other through the cycle tracking journey. With automatic notifications, easy-to-use interface, and secure messaging, partners can stay connected and supportive!

---

**Status**: ✅ Complete & Ready
**Version**: 1.0
**Last Updated**: October 20, 2025
