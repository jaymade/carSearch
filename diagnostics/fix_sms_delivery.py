#!/usr/bin/env python3
"""
Script to help fix SMS delivery issues with Twilio
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def check_twilio_setup():
    """Check and potentially fix Twilio configuration for better delivery"""
    
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    to_number = os.getenv('TARGET_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, from_number, to_number]):
        print("❌ Missing Twilio credentials in .env file")
        return
    
    client = Client(account_sid, auth_token)
    
    print("📱 Twilio SMS Delivery Diagnostic")
    print("=" * 40)
    
    # Check account status
    try:
        account = client.api.accounts(account_sid).fetch()
        print(f"✅ Account Status: {account.status}")
        print(f"📞 From Number: {from_number}")
        print(f"📱 To Number: {to_number}")
    except Exception as e:
        print(f"❌ Account Error: {e}")
        return
    
    # Check recent messages
    print("\n📋 Recent Message Status:")
    try:
        messages = client.messages.list(limit=5)
        for msg in messages:
            status_icon = "✅" if msg.status == "delivered" else "⚠️" if msg.status == "sent" else "❌"
            print(f"{status_icon} {msg.date_created.strftime('%m/%d %H:%M')} - {msg.status} - {msg.error_code or 'No error'}")
            
            if msg.error_code:
                error_meanings = {
                    30034: "Carrier blocked - Contact carrier to whitelist",
                    30003: "Unreachable destination - Check number format", 
                    30006: "Landline or invalid mobile number",
                    30008: "Unknown error - Try different message content"
                }
                print(f"      🔍 {error_meanings.get(msg.error_code, 'Unknown error code')}")
                
    except Exception as e:
        print(f"❌ Message History Error: {e}")
    
    # Suggest fixes
    print("\n🔧 Suggested Fixes:")
    print("1. Contact your carrier (most effective):")
    print("   - Call customer service")
    print("   - Ask to whitelist Twilio numbers")
    print("   - Mention 'business SMS notifications'")
    
    print("\n2. Verify your phone number with Twilio:")
    print("   - Go to console.twilio.com")
    print("   - Phone Numbers → Manage → Verified Caller IDs")
    print("   - Add and verify your number")
    
    print("\n3. Try a different Twilio number:")
    print("   - Buy a local area code number")
    print("   - Local numbers have better delivery rates")
    
    print("\n4. Check message content:")
    print("   - Avoid spam trigger words")
    print("   - Keep messages short and clear")
    print("   - Add your business name")

def send_test_with_different_format():
    """Send a test message with carrier-friendly format"""
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    to_number = os.getenv('TARGET_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, from_number, to_number]):
        print("❌ Missing Twilio credentials")
        return
    
    client = Client(account_sid, auth_token)
    
    # Try a very simple, carrier-friendly message
    simple_message = "AutoPark Honda: New Honda Civic available. Call 919-467-6100 or visit autoparkhonda.com"
    
    try:
        message = client.messages.create(
            body=simple_message,
            from_=from_number,
            to=f"+1{to_number}" if not to_number.startswith('+') else to_number
        )
        
        print(f"✅ Test message sent with SID: {message.sid}")
        print("📝 Message: ", simple_message)
        print("\nThis format may have better delivery rates.")
        
    except Exception as e:
        print(f"❌ Error sending test: {e}")

if __name__ == "__main__":
    check_twilio_setup()
    
    print("\n" + "=" * 40)
    response = input("Send a carrier-friendly test message? (y/n): ")
    if response.lower() == 'y':
        send_test_with_different_format()