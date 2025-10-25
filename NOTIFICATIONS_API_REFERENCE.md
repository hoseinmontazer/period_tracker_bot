# Notifications API Reference

Complete API documentation for the notifications system including partner messaging, system notifications, and preferences.

---

## Base URL
```
https://api-period.shirpala.ir/api/notifications/
```

## Authentication
All endpoints require Bearer token authentication:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## 📬 System Notifications

### 1. List All Notifications

**Endpoint:** `GET /api/notifications/notifications/`

**Description:** Get all notifications for the authenticated user

**Request:**
```bash
curl 'https://api-period.shirpala.ir/api/notifications/notifications/' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "notification_type": "period_reminder",
    "title": "Period Coming Soon",
    "message": "Your period is expected in 2 days on January 25.",
    "is_read": false,
    "created_at": "2025-01-23T09:00:00Z",
    "read_at": null,
    "related_id": 5,
    "related_type": "period"
  },
  {
    "id": 2,
    "notification_type": "ovulation",
    "title": "Ovulation Window",
    "message": "You are in your ovulation window (Day 14 of your cycle).",
    "is_read": true,
    "created_at": "2025-01-20T09:00:00Z",
    "read_at": "2025-01-20T10:30:00Z",
    "related_id": 5,
    "related_type": "period"
  }
]
```

---

### 2. Get Unread Notifications

**Endpoint:** `GET /api/notifications/notifications/unread/`

**Description:** Get only unread notifications

**Request:**
```bash
curl 'https://api-period.shirpala.ir/api/notifications/notifications/unread/' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**Response:** `200 OK`
```json
{
  "count": 3,
  "notifications": [
    {
      "id": 1,
      "notification_type": "period_reminder",
      "title": "Period Coming Soon",
      "message": "Your period is expected in 2 days.",
      "is_read": false,
      "created_at": "2025-01-23T09:00:00Z"
    },
    {
      "id": 3,
      "notification_type": "partner_message",
      "title": "New message from partner",
      "message": "John sent you a message",
      "is_read": false,
      "created_at": "2025-01-23T10:15:00Z"
    }
  ]
}
```

---

### 3. Mark Notification as Read

**Endpoint:** `POST /api/notifications/notifications/{id}/mark_read/`

**Description:** Mark a specific notification as read

**Request:**
```bash
curl -X POST 'https://api-period.shirpala.ir/api/notifications/notifications/1/mark_read/' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**Response:** `200 OK`
```json
{
  "status": "success",
  "notification": {
    "id": 1,
    "notification_type": "period_reminder",
    "title": "Period Coming Soon",
    "message": "Your period is expected in 2 days.",
    "is_read": true,
    "created_at": "2025-01-23T09:00:00Z",
    "read_at": "2025-01-23T11:30:00Z"
  }
}
```

---

### 4. Mark All as Read

**Endpoint:** `POST /api/notifications/notifications/mark_all_read/`

**Description:** Mark all notifications as read

**Request:**
```bash
curl -X POST 'https://api-period.shirpala.ir/api/notifications/notifications/mark_all_read/' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**Response:** `200 OK`
```json
{
  "status": "success",
  "marked_read": 5
}
```

---

### 5. Delete Notification

**Endpoint:** `DELETE /api/notifications/notifications/{id}/`

**Description:** Delete a specific notification

**Request:**
```bash
curl -X DELETE 'https://api-period.shirpala.ir/api/notifications/notifications/1/' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**Response:** `204 No Content`

---

## 💬 Partner Messages

### 1. Send Message to Partner

**Endpoint:** `POST /api/notifications/messages/`

**Description:** Send a message to your partner

**Request:**
```bash
curl -X POST 'https://api-period.shirpala.ir/api/notifications/messages/' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "receiver": 2,
    "message": "How are you feeling today?"
  }'
```

**Request Body:**
```json
{
  "receiver": 2,
  "message": "How are you feeling today?"
}
```

**Response:** `201 Created`
```json
{
  "id": 15,
  "sender": 1,
  "sender_username": "john_doe",
  "sender_name": "John Doe",
  "receiver": 2,
  "receiver_username": "jane_doe",
  "receiver_name": "Jane Doe",
  "message": "How are you feeling today?",
  "is_read": false,
  "created_at": "2025-01-23T14:30:00Z",
  "read_at": null
}
```

**Error Response:** `400 Bad Request`
```json
{
  "error": "You can only send messages to your partner"
}
```

---

### 2. Get All Messages

**Endpoint:** `GET /api/notifications/messages/`

**Description:** Get all messages (sent and received)

**Request:**
```bash
curl 'https://api-period.shirpala.ir/api/notifications/messages/' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**Response:** `200 OK`
```json
[
  {
    "id": 15,
    "sender_name": "John Doe",
    "receiver_name": "Jane Doe",
    "message": "How are you feeling today?",
    "is_read": true,
    "created_at": "2025-01-23T14:30:00Z",
    "read_at": "2025-01-23T14:35:00Z"
  },
  {
    "id": 14,
    "sender_name": "Jane Doe",
    "receiver_name": "John Doe",
    "message": "I'm doing well, thanks!",
    "is_read": true,
    "created_at": "2025-01-23T14:25:00Z",
    "read_at": "2025-01-23T14:26:00Z"
  }
]
```

---

### 3. Get Conversation with Partner

**Endpoint:** `GET /api/notifications/messages/conversation/?partner_id={id}`

**Description:** Get full conversation with a specific partner

**Request:**
```bash
curl 'https://api-period.shirpala.ir/api/notifications/messages/conversation/?partner_id=2' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**Response:** `200 OK`
```json
{
  "count": 10,
  "messages": [
    {
      "id": 10,
      "sender_name": "John Doe",
      "receiver_name": "Jane Doe",
      "message": "Good morning!",
      "is_read": true,
      "created_at": "2025-01-23T08:00:00Z"
    },
    {
      "id": 11,
      "sender_name": "Jane Doe",
      "receiver_name": "John Doe",
      "message": "Good morning! How did you sleep?",
      "is_read": true,
      "created_at": "2025-01-23T08:05:00Z"
    },
    {
      "id": 12,
      "sender_name": "John Doe",
      "receiver_name": "Jane Doe",
      "message": "Pretty well, thanks!",
      "is_read": true,
      "created_at": "2025-01-23T08:10:00Z"
    }
  ]
}
```

**Note:** This endpoint automatically marks received messages as read.

---

### 4. Get Unread Messages

**Endpoint:** `GET /api/notifications/messages/unread/`

**Description:** Get unread messages from partner

**Request:**
```bash
curl 'https://api-period.shirpala.ir/api/notifications/messages/unread/' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**Response:** `200 OK`
```json
{
  "count": 2,
  "messages": [
    {
      "id": 16,
      "sender_name": "Jane Doe",
      "receiver_name": "John Doe",
      "message": "Don't forget to pick up groceries!",
      "is_read": false,
      "created_at": "2025-01-23T15:00:00Z"
    },
    {
      "id": 17,
      "sender_name": "Jane Doe",
      "receiver_name": "John Doe",
      "message": "Thanks for being supportive ❤️",
      "is_read": false,
      "created_at": "2025-01-23T15:30:00Z"
    }
  ]
}
```

---

## 📱 Push Notification Tokens

### 1. Register Push Token

**Endpoint:** `POST /api/notifications/push-tokens/`

**Description:** Register a device for push notifications

**Request:**
```bash
curl -X POST 'https://api-period.shirpala.ir/api/notifications/push-tokens/' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "device_type": "ios",
    "token": "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]"
  }'
```

**Request Body:**
```json
{
  "device_type": "ios",
  "token": "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]"
}
```

**Device Types:**
- `ios` - iOS devices
- `android` - Android devices
- `web` - Web push notifications

**Response:** `201 Created`
```json
{
  "id": 5,
  "device_type": "ios",
  "token": "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]",
  "is_active": true,
  "created_at": "2025-01-23T16:00:00Z",
  "updated_at": "2025-01-23T16:00:00Z"
}
```

---

### 2. List Push Tokens

**Endpoint:** `GET /api/notifications/push-tokens/`

**Description:** Get all registered push tokens for the user

**Request:**
```bash
curl 'https://api-period.shirpala.ir/api/notifications/push-tokens/' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**Response:** `200 OK`
```json
[
  {
    "id": 5,
    "device_type": "ios",
    "token": "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]",
    "is_active": true,
    "created_at": "2025-01-23T16:00:00Z"
  },
  {
    "id": 3,
    "device_type": "android",
    "token": "fcm_token_xxxxxxxxxxxxxxxxxx",
    "is_active": false,
    "created_at": "2025-01-20T10:00:00Z"
  }
]
```

---

### 3. Delete Push Token

**Endpoint:** `DELETE /api/notifications/push-tokens/{id}/`

**Description:** Remove a push token (e.g., when user logs out)

**Request:**
```bash
curl -X DELETE 'https://api-period.shirpala.ir/api/notifications/push-tokens/5/' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**Response:** `204 No Content`

---

## ⚙️ Notification Preferences

### 1. Get Preferences

**Endpoint:** `GET /api/notifications/preferences/`

**Description:** Get user's notification preferences

**Request:**
```bash
curl 'https://api-period.shirpala.ir/api/notifications/preferences/' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

**Response:** `200 OK`
```json
{
  "email_period_reminder": true,
  "email_ovulation": true,
  "email_partner_message": true,
  "email_wellness_reminder": false,
  "push_period_reminder": true,
  "push_ovulation": true,
  "push_partner_message": true,
  "push_wellness_reminder": false,
  "inapp_period_reminder": true,
  "inapp_ovulation": true,
  "inapp_partner_message": true,
  "inapp_wellness_reminder": true,
  "reminder_days_before": 2,
  "reminder_time": "09:00:00"
}
```

---

### 2. Update Preferences

**Endpoint:** `PUT /api/notifications/preferences/`

**Description:** Update notification preferences (partial update supported)

**Request:**
```bash
curl -X PUT 'https://api-period.shirpala.ir/api/notifications/preferences/' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "push_period_reminder": false,
    "reminder_days_before": 3,
    "reminder_time": "08:00:00"
  }'
```

**Request Body (all fields optional):**
```json
{
  "email_period_reminder": true,
  "email_ovulation": true,
  "email_partner_message": true,
  "email_wellness_reminder": false,
  "push_period_reminder": false,
  "push_ovulation": true,
  "push_partner_message": true,
  "push_wellness_reminder": false,
  "inapp_period_reminder": true,
  "inapp_ovulation": true,
  "inapp_partner_message": true,
  "inapp_wellness_reminder": true,
  "reminder_days_before": 3,
  "reminder_time": "08:00:00"
}
```

**Response:** `200 OK`
```json
{
  "email_period_reminder": true,
  "email_ovulation": true,
  "email_partner_message": true,
  "email_wellness_reminder": false,
  "push_period_reminder": false,
  "push_ovulation": true,
  "push_partner_message": true,
  "push_wellness_reminder": false,
  "inapp_period_reminder": true,
  "inapp_ovulation": true,
  "inapp_partner_message": true,
  "inapp_wellness_reminder": true,
  "reminder_days_before": 3,
  "reminder_time": "08:00:00"
}
```

---

## 📊 Notification Types

### System Notification Types

| Type | Description | When Triggered |
|------|-------------|----------------|
| `period_reminder` | Period coming soon | X days before period (configurable) |
| `period_approaching` | Period tomorrow | 1 day before period |
| `ovulation` | Ovulation window | Day 14 of cycle (or calculated) |
| `fertile_window` | Fertile window | 5 days before to 1 day after ovulation |
| `pms_warning` | PMS phase | 3-4 days before period |
| `wellness_reminder` | Log wellness data | Daily if not logged |
| `partner_message` | New partner message | When partner sends message |
| `system` | System notification | Various system events |

---

## 🔔 Error Responses

### 400 Bad Request
```json
{
  "error": "partner_id is required"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "You can only send messages to your partner"
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## 💡 Usage Examples

### Example 1: Check for New Messages
```javascript
// Check unread messages count
const response = await fetch('/api/notifications/messages/unread/', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const data = await response.json();

if (data.count > 0) {
  showNotificationBadge(data.count);
}
```

### Example 2: Send Message and Show Confirmation
```javascript
const sendMessage = async (partnerId, message) => {
  const response = await fetch('/api/notifications/messages/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      receiver: partnerId,
      message: message
    })
  });
  
  if (response.ok) {
    const data = await response.json();
    console.log('Message sent:', data);
    return data;
  }
};
```

### Example 3: Load Conversation
```javascript
const loadConversation = async (partnerId) => {
  const response = await fetch(
    `/api/notifications/messages/conversation/?partner_id=${partnerId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  const data = await response.json();
  displayMessages(data.messages);
};
```

### Example 4: Update Notification Preferences
```javascript
const updatePreferences = async (preferences) => {
  const response = await fetch('/api/notifications/preferences/', {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(preferences)
  });
  
  return await response.json();
};

// Example usage
updatePreferences({
  push_period_reminder: true,
  reminder_days_before: 3
});
```

---

## 🔄 Polling vs WebSocket

### Current: Polling
```javascript
// Poll for new notifications every 30 seconds
setInterval(async () => {
  const response = await fetch('/api/notifications/notifications/unread/');
  const data = await response.json();
  updateNotificationUI(data);
}, 30000);
```

### Future: WebSocket (Coming Soon)
```javascript
// Real-time notifications via WebSocket
const ws = new WebSocket('wss://api-period.shirpala.ir/ws/notifications/');
ws.onmessage = (event) => {
  const notification = JSON.parse(event.data);
  showNotification(notification);
};
```

---

## 📝 Notes

1. **Authentication Required:** All endpoints require a valid Bearer token
2. **Partner Verification:** Messages can only be sent to linked partners
3. **Auto Read Receipts:** Conversation endpoint marks messages as read automatically
4. **Pagination:** Not currently implemented, may be added for large datasets
5. **Rate Limiting:** Consider implementing rate limiting for message sending
6. **Push Notifications:** Requires additional setup (Firebase/APNs)

---

## 🆘 Support

For issues or questions:
- Check error responses for details
- Verify authentication token is valid
- Ensure partner relationship exists before messaging
- Check notification preferences are enabled

---

**Last Updated:** January 2025  
**API Version:** v1.0
