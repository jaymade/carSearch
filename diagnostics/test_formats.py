#!/usr/bin/env python3
"""
Try different message formats to bypass carrier blocks
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client
import time

load_dotenv()

def try_different_formats():
    """Try several different message formats"""
    
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    to_number = os.getenv('TARGET_PHONE_NUMBER')
    
    client = Client(account_sid, auth_token)
    formatted_number = f"+1{to_number}" if not to_number.startswith('+') else to_number
    
    # Try different message formats
    messages = [
        "Hello from Jay's app",
        "Test 123",
        "Car alert: Honda available",
        "AutoPark Honda notification",
        "Jay - your car search found matches"
    ]
    
    for i, msg in enumerate(messages, 1):
        try:
            print(f"\n📱 Test {i}: '{msg}'")
            
            message = client.messages.create(
                body=msg,
                from_=from_number,
                to=formatted_number
            )
            
            print(f"✅ Sent - SID: {message.sid}")
            
            # Check status after a moment
            time.sleep(2)
            updated = client.messages(message.sid).fetch()
            
            if updated.error_code:
                print(f"❌ Status: {updated.status} - Error {updated.error_code}")
            else:
                print(f"✅ Status: {updated.status}")
                if updated.status in ['sent', 'delivered']:
                    print(f"🎉 SUCCESS! This format worked: '{msg}'")
                    break
                    
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)  # Rate limiting

if __name__ == "__main__":
    try_different_formats()