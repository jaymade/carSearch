#!/usr/bin/env python3
"""
Get a local 919 area code number from Twilio for better SMS delivery
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def get_local_number():
    """Search for and purchase a local 919 area code number"""
    
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    
    if not all([account_sid, auth_token]):
        print("❌ Missing Twilio credentials")
        return
    
    client = Client(account_sid, auth_token)
    
    print("🔍 Searching for local 919 area code numbers...")
    
    try:
        # Search for available numbers in 919 area code
        available_numbers = client.available_phone_numbers('US').local.list(
            area_code=919,
            sms_enabled=True,
            limit=10
        )
        
        if available_numbers:
            print(f"📞 Found {len(available_numbers)} available 919 numbers:")
            for i, number in enumerate(available_numbers[:5]):
                print(f"  {i+1}. {number.phone_number}")
            
            choice = input(f"\nBuy number 1-{min(len(available_numbers), 5)} or 'n' to skip: ")
            
            if choice.isdigit() and 1 <= int(choice) <= len(available_numbers):
                selected = available_numbers[int(choice) - 1]
                
                # Purchase the number
                purchased = client.incoming_phone_numbers.create(
                    phone_number=selected.phone_number
                )
                
                print(f"✅ Successfully purchased: {purchased.phone_number}")
                print(f"💡 Update your .env file:")
                print(f"   TWILIO_PHONE_NUMBER={purchased.phone_number}")
                
                return purchased.phone_number
                
        else:
            print("❌ No available 919 numbers found")
            
    except Exception as e:
        print(f"❌ Error searching for numbers: {e}")

if __name__ == "__main__":
    get_local_number()