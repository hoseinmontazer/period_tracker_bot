# 🧪 Test Partner Messaging System

## Issue Fixed ✅

**Problem**: Partner ID was not being extracted correctly from the API response.

**Solution**: Updated to use `partner_user_id` field from the API response.

---

## API Response Format

Your API returns partner information like this:
```json
{
  "partners": [
    {
      "username": "Zara",
      "email": "shadij1989@gmail.com",
      "partner_user_id": 7
    }
  ]
}
```

The code now correctly extracts `partner_user_id` (value: 7) to use for messaging.

---

## Testing Steps

### 1. Verify Partner is Linked

```bash
# In Telegram
/start
→ Login
→ Partner Menu
→ Should see partner "Zara"
```

### 2. Test Messaging

```bash
# Open messages
/messages

# You should see:
💬 Partner Messages
Choose an option:
[💬 View Conversation]
[✉️ Send Message]
[📋 All Messages]
[⬅️ Back to Dashboard]
```

### 3. Send a Test Message

```bash
# Click "✉️ Send Message"
# Bot should show:
✉️ Send Message to Zara
Type your message below:

# Type: "Hello Zara!"
# Bot should respond:
✅ Message sent to Zara!
💬 Your message: Hello Zara!
```

### 4. View Conversation

```bash
# Click "💬 View Conversation"
# Should show your message:
💬 Conversation with Zara
Total messages: 1

──────────────────────────────

🙋 You (03:45 PM):
Hello Zara!
```

---

## Expected Behavior

### ✅ Success Indicators

1. **Partner ID Found**
   - No "Partner information not found" error
   - Partner name displays correctly (Zara)

2. **Message Sent**
   - Confirmation message appears
   - No API errors

3. **Conversation Loads**
   - Messages display correctly
   - Timestamps show properly
   - Sender names are correct

### ❌ Error Messages (If Any)

| Error | Cause | Solution |
|-------|-------|----------|
| "Partner information not found" | No partner linked | Link a partner first |
| "Partner ID not found" | API response issue | Check API response format |
| "Failed to send message" | API error | Check token, try again |
| "You don't have any partners linked" | No partners | Add partner via invitation |

---

## Debug Information

### Check Partner Data

Add this temporary debug code to see what the API returns:

```python
# In messaging_handlers.py, after getting profile:
partners = profile.get("partners", [])
print(f"DEBUG: Partners data: {partners}")

if partners:
    partner = partners[0]
    print(f"DEBUG: Partner object: {partner}")
    partner_id = partner.get("partner_user_id") or partner.get("id")
    print(f"DEBUG: Extracted partner_id: {partner_id}")
```

### Check API Response

```bash
# Test the profile API directly
curl --location 'https://api-period.shirpala.ir/api/user/profile/' \
--header 'Authorization: Bearer YOUR_TOKEN'

# Should return:
{
  "partners": [
    {
      "username": "Zara",
      "email": "shadij1989@gmail.com",
      "partner_user_id": 7
    }
  ]
}
```

---

## What Was Fixed

### Before (Broken)
```python
partner_id = partner.get("id")  # ❌ Returns None
```

### After (Fixed)
```python
partner_id = partner.get("partner_user_id") or partner.get("id")  # ✅ Returns 7
```

### Added Error Handling
```python
if not partner_id:
    await update.message.reply_text("❌ Partner ID not found...")
    return DASHBOARD
```

---

## Testing Checklist

- [ ] Bot starts without errors
- [ ] `/messages` command works
- [ ] Partner name displays correctly (Zara)
- [ ] Can click "Send Message"
- [ ] Message input prompt appears
- [ ] Can type and send message
- [ ] Confirmation message appears
- [ ] Can view conversation
- [ ] Messages display correctly
- [ ] No "Partner information not found" error

---

## API Endpoints Being Used

### 1. Get Profile (to get partner_user_id)
```
GET /api/user/profile/
Response: { "partners": [{ "partner_user_id": 7, ... }] }
```

### 2. Send Message
```
POST /api/notifications/messages/
Body: { "receiver": 7, "message": "Hello!" }
```

### 3. Get Conversation
```
GET /api/notifications/messages/conversation/?partner_id=7
```

### 4. Get Unread Messages
```
GET /api/notifications/messages/unread/
```

---

## Common Issues & Solutions

### Issue 1: "Partner information not found"
**Cause**: `partner_user_id` was not being extracted
**Status**: ✅ FIXED
**Solution**: Code now correctly uses `partner_user_id`

### Issue 2: Partner name shows but can't send
**Cause**: Partner ID is None
**Status**: ✅ FIXED
**Solution**: Added fallback and error handling

### Issue 3: API returns 400 error
**Possible causes**:
- Invalid partner_id
- Partner not linked
- Token expired

**Solution**:
- Verify partner is linked
- Check token is valid
- Re-login if needed

---

## Next Steps

1. **Test the fix**:
   ```bash
   python bot.py
   # Then test in Telegram
   ```

2. **Verify partner ID**:
   - Should extract `7` from the API response
   - Should use it for messaging

3. **Send test message**:
   - Message should go to partner with ID 7
   - Should see confirmation

4. **Check logs**:
   - Look for any errors
   - Verify API calls succeed

---

## Success Criteria

✅ Your messaging system is working when:
- Partner name displays: "Zara"
- Partner ID extracted: 7
- Can send messages without errors
- Messages appear in conversation
- No "Partner information not found" error

---

## Support

If you still see issues:

1. **Check the logs**:
   ```bash
   tail -f bot.log
   ```

2. **Verify API response**:
   - Make sure `partner_user_id` is in the response
   - Check the value is correct (7)

3. **Test API directly**:
   ```bash
   # Send message via curl
   curl -X POST 'https://api-period.shirpala.ir/api/notifications/messages/' \
     -H 'Authorization: Bearer YOUR_TOKEN' \
     -H 'Content-Type: application/json' \
     -d '{"receiver": 7, "message": "Test"}'
   ```

---

**Status**: ✅ Fixed
**Issue**: Partner ID extraction
**Solution**: Use `partner_user_id` field
**Ready to test**: Yes!
