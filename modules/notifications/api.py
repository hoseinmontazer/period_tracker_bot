"""API functions for notification management"""
import aiohttp
from config import BASE_URL


async def get_notifications(token: str):
    """Get all notifications for the user"""
    url = f"{BASE_URL}api/notifications/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to fetch notifications: {response.status}"}


async def get_unread_notifications(token: str):
    """Get unread notifications for the user"""
    url = f"{BASE_URL}api/notifications/notifications/unread/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to fetch unread notifications: {response.status}"}


async def mark_notification_read(token: str, notification_id: int):
    """Mark a specific notification as read"""
    url = f"{BASE_URL}api/notifications/{notification_id}/mark_read/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to mark notification as read: {response.status}"}


async def mark_all_notifications_read(token: str):
    """Mark all notifications as read"""
    url = f"{BASE_URL}api/notifications/mark_all_read/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to mark all notifications as read: {response.status}"}


async def clear_old_notifications(token: str):
    """Clear old read notifications"""
    url = f"{BASE_URL}api/notifications/clear_old/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to clear old notifications: {response.status}"}


async def get_notification_preferences(token: str):
    """Get user's notification preferences"""
    url = f"{BASE_URL}api/notification-preferences/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to fetch notification preferences: {response.status}"}


async def update_notification_preferences(token: str, preferences: dict):
    """Update user's notification preferences"""
    url = f"{BASE_URL}api/notification-preferences/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers, json=preferences) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to update notification preferences: {response.status}"}


async def generate_notifications(token: str):
    """Generate notifications based on cycle data"""
    url = f"{BASE_URL}api/generate-notifications/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to generate notifications: {response.status}"}


# ============================================================================
# PARTNER MESSAGING API
# ============================================================================

async def send_partner_message(token: str, receiver_id: int, message: str):
    """Send a message to partner"""
    url = f"{BASE_URL}api/notifications/notifications/messages/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "receiver": receiver_id,
        "message": message
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 201:
                return await response.json()
            elif response.status == 400:
                error_data = await response.json()
                return {"error": error_data.get("error", "Bad request")}
            return {"error": f"Failed to send message: {response.status}"}


async def get_all_messages(token: str):
    """Get all messages (sent and received)"""
    url = f"{BASE_URL}api/notifications/messages/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to fetch messages: {response.status}"}


async def get_conversation_with_partner(token: str, partner_id: int):
    """Get full conversation with a specific partner"""
    url = f"{BASE_URL}api/notifications/messages/conversation/?partner_id={partner_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to fetch conversation: {response.status}"}


async def get_unread_messages(token: str):
    """Get unread messages from partner"""
    url = f"{BASE_URL}api/notifications/messages/unread/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to fetch unread messages: {response.status}"}


# ============================================================================
# PUSH NOTIFICATION TOKENS API
# ============================================================================

async def register_push_token(token: str, device_type: str, push_token: str):
    """Register a device for push notifications"""
    url = f"{BASE_URL}api/notifications/push-tokens/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "device_type": device_type,  # "ios", "android", or "web"
        "token": push_token
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 201:
                return await response.json()
            return {"error": f"Failed to register push token: {response.status}"}


async def get_push_tokens(token: str):
    """Get all registered push tokens for the user"""
    url = f"{BASE_URL}api/notifications/push-tokens/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to fetch push tokens: {response.status}"}


async def delete_push_token(token: str, token_id: int):
    """Remove a push token"""
    url = f"{BASE_URL}api/notifications/push-tokens/{token_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                return {"status": "success", "message": "Push token deleted"}
            return {"error": f"Failed to delete push token: {response.status}"}


# ============================================================================
# SYSTEM NOTIFICATIONS API (Updated endpoints)
# ============================================================================

async def get_system_notifications(token: str):
    """Get all system notifications (updated endpoint)"""
    url = f"{BASE_URL}api/notifications/notifications/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to fetch notifications: {response.status}"}


async def get_unread_system_notifications(token: str):
    """Get unread system notifications (updated endpoint)"""
    url = f"{BASE_URL}api/notifications/notifications/unread/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to fetch unread notifications: {response.status}"}


async def mark_system_notification_read(token: str, notification_id: int):
    """Mark a specific system notification as read (updated endpoint)"""
    url = f"{BASE_URL}api/notifications/notifications/{notification_id}/mark_read/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to mark notification as read: {response.status}"}


async def mark_all_system_notifications_read(token: str):
    """Mark all system notifications as read (updated endpoint)"""
    url = f"{BASE_URL}api/notifications/notifications/mark_all_read/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to mark all notifications as read: {response.status}"}


async def delete_system_notification(token: str, notification_id: int):
    """Delete a specific system notification"""
    url = f"{BASE_URL}api/notifications/notifications/{notification_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                return {"status": "success", "message": "Notification deleted"}
            return {"error": f"Failed to delete notification: {response.status}"}


# ============================================================================
# NOTIFICATION PREFERENCES API (Updated)
# ============================================================================

async def get_preferences(token: str):
    """Get user's notification preferences (updated endpoint)"""
    url = f"{BASE_URL}api/notifications/preferences/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to fetch preferences: {response.status}"}


async def update_preferences(token: str, preferences: dict):
    """Update notification preferences (updated endpoint)"""
    url = f"{BASE_URL}api/notifications/preferences/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers, json=preferences) as response:
            if response.status == 200:
                return await response.json()
            return {"error": f"Failed to update preferences: {response.status}"}
