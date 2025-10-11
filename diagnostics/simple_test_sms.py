#!/usr/bin/env python3
"""
Send a very simple test SMS to check delivery
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def send_simple_test():
    """Send the simplest possible test message"""
    
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    to_number = os.getenv('TARGET_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, from_number]):
        print("❌ Missing Twilio credentials")
        return
    
    client = Client(account_sid, auth_token)
    
    # Very simple message to avoid spam filters
    simple_message = "Test message from your car search app. Reply STOP to opt out."
    
    try:
        # Ensure proper phone number format
        formatted_number = f"+1{to_number}" if not to_number.startswith('+') else to_number
        
        print(f"📱 Sending test to: {formatted_number}")
        print(f"📝 Message: {simple_message}")
        
        message = client.messages.create(
            body=simple_message,
            from_=from_number,
            to=formatted_number
        )
        
        print(f"✅ Message sent successfully!")
        print(f"🆔 SID: {message.sid}")
        print(f"📊 Status: {message.status}")
        
        # Wait a moment and check status
        import time
        time.sleep(3)
        
        updated_message = client.messages(message.sid).fetch()
        print(f"🔄 Updated status: {updated_message.status}")
        
        if updated_message.error_code:
            print(f"❌ Error code: {updated_message.error_code}")
        else:
            print("✅ No errors detected")
            
        return message.sid
        
    except Exception as e:
        print(f"❌ Error sending message: {e}")

if __name__ == "__main__":
    send_simple_test()