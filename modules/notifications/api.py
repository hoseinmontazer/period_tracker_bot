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
    url = f"{BASE_URL}api/notifications/unread/"
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
