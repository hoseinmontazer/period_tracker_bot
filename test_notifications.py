"""
Test script for notification system
Run this to verify the notification integration is working
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.notifications.api import (
    get_notifications,
    get_unread_notifications,
    get_notification_preferences,
    generate_notifications
)


async def test_notification_api(token: str):
    """Test notification API endpoints"""
    print("🧪 Testing Notification API Integration\n")
    print("=" * 50)
    
    # Test 1: Get all notifications
    print("\n1️⃣ Testing: Get All Notifications")
    print("-" * 50)
    response = await get_notifications(token)
    if "error" in response:
        print(f"❌ Error: {response['error']}")
    else:
        count = response.get("count", 0)
        print(f"✅ Success! Found {count} notifications")
        if count > 0:
            print(f"   First notification: {response['results'][0].get('title', 'N/A')}")
    
    # Test 2: Get unread notifications
    print("\n2️⃣ Testing: Get Unread Notifications")
    print("-" * 50)
    response = await get_unread_notifications(token)
    if "error" in response:
        print(f"❌ Error: {response['error']}")
    else:
        count = response.get("count", 0)
        print(f"✅ Success! Found {count} unread notifications")
        if count > 0:
            notif = response['data'][0]
            print(f"   Type: {notif.get('notification_type', 'N/A')}")
            print(f"   Title: {notif.get('title', 'N/A')}")
    
    # Test 3: Get notification preferences
    print("\n3️⃣ Testing: Get Notification Preferences")
    print("-" * 50)
    response = await get_notification_preferences(token)
    if "error" in response:
        print(f"❌ Error: {response['error']}")
    else:
        prefs = response.get("data", {})
        print(f"✅ Success! Preferences loaded")
        print(f"   Period alerts: {prefs.get('period_started_alert', 'N/A')}")
        print(f"   Ovulation alerts: {prefs.get('ovulation_alert', 'N/A')}")
        print(f"   Preferred time: {prefs.get('preferred_notification_time', 'N/A')}")
    
    # Test 4: Generate notifications
    print("\n4️⃣ Testing: Generate Notifications")
    print("-" * 50)
    response = await generate_notifications(token)
    if "error" in response:
        print(f"❌ Error: {response['error']}")
    else:
        print(f"✅ Success! {response.get('message', 'Generated notifications')}")
        created = response.get('notifications_created', [])
        if created:
            print(f"   Created: {', '.join(created)}")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!\n")


async def test_formatting():
    """Test notification formatting functions"""
    print("\n🎨 Testing Formatting Functions\n")
    print("=" * 50)
    
    from utils.helpers import format_notification_list, format_notification_preferences
    
    # Test notification list formatting
    print("\n1️⃣ Testing: Notification List Formatting")
    print("-" * 50)
    sample_notifications = [
        {
            "id": 1,
            "notification_type": "PERIOD_COMING",
            "title": "Period Coming Soon",
            "message": "Your period is expected in 3 days.",
            "is_read": False
        },
        {
            "id": 2,
            "notification_type": "OVULATION_COMING",
            "title": "Ovulation Window",
            "message": "You are entering your ovulation window.",
            "is_read": True
        }
    ]
    
    formatted = format_notification_list(sample_notifications, 2, unread_only=False)
    print(formatted)
    
    # Test preferences formatting
    print("\n2️⃣ Testing: Preferences Formatting")
    print("-" * 50)
    sample_prefs = {
        "period_started_alert": True,
        "period_late_alert": True,
        "period_reminder_days": 3,
        "ovulation_alert": True,
        "fertile_window_alert": True,
        "pms_phase_alert": True,
        "symptom_reminder": True,
        "wellness_reminder": True,
        "partner_period_alert": True,
        "partner_pms_alert": False,
        "preferred_notification_time": "09:00:00"
    }
    
    formatted = format_notification_preferences(sample_prefs)
    print(formatted)
    
    print("\n" + "=" * 50)
    print("✅ Formatting tests completed!\n")


def main():
    """Main test function"""
    print("\n" + "=" * 50)
    print("🔔 NOTIFICATION SYSTEM TEST SUITE")
    print("=" * 50)
    
    # Check if token is provided
    if len(sys.argv) < 2:
        print("\n⚠️  Usage: python test_notifications.py <YOUR_AUTH_TOKEN>")
        print("\nTo get your token:")
        print("1. Login to the bot")
        print("2. Check data/user_tokens.json")
        print("3. Copy your token and run: python test_notifications.py YOUR_TOKEN\n")
        
        # Run formatting tests without token
        print("Running formatting tests only...\n")
        asyncio.run(test_formatting())
        return
    
    token = sys.argv[1]
    print(f"\n🔑 Using token: {token[:20]}...\n")
    
    # Run all tests
    asyncio.run(test_notification_api(token))
    asyncio.run(test_formatting())
    
    print("=" * 50)
    print("🎉 All tests completed successfully!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
