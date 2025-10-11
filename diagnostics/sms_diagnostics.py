#!/usr/bin/env python3
"""
SMS Diagnostic Script - Help troubleshoot SMS delivery issues
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from sms_notifier import SMSNotifier
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, TARGET_PHONE_NUMBER

def run_sms_diagnostics():
    """Run comprehensive SMS diagnostics"""
    
    print("📱 SMS Delivery Diagnostic Tool")
    print("=" * 50)
    
    # Check configuration
    print("\n1. Configuration Check:")
    print(f"   Twilio Account SID: {TWILIO_ACCOUNT_SID[:10]}..." if TWILIO_ACCOUNT_SID else "   ❌ Missing Account SID")
    print(f"   Twilio Auth Token: {TWILIO_AUTH_TOKEN[:10]}..." if TWILIO_AUTH_TOKEN else "   ❌ Missing Auth Token")
    print(f"   From Phone Number: {TWILIO_PHONE_NUMBER}")
    print(f"   To Phone Number: {TARGET_PHONE_NUMBER}")
    
    # Validate phone number format
    print("\n2. Phone Number Format Check:")
    if TARGET_PHONE_NUMBER.startswith('+1') and len(TARGET_PHONE_NUMBER) == 12:
        print("   ✅ Target phone number format looks correct")
    else:
        print("   ⚠️  Target phone number should be in format +1XXXXXXXXXX")
        print(f"      Current format: {TARGET_PHONE_NUMBER}")
    
    if TWILIO_PHONE_NUMBER.startswith('+1') and len(TWILIO_PHONE_NUMBER) == 12:
        print("   ✅ Twilio phone number format looks correct")
    else:
        print("   ⚠️  Twilio phone number should be in format +1XXXXXXXXXX")
        print(f"      Current format: {TWILIO_PHONE_NUMBER}")
    
    # Test Twilio connection
    print("\n3. Twilio Connection Test:")
    notifier = SMSNotifier()
    if notifier.client:
        print("   ✅ Twilio client initialized successfully")
        
        # Try to get account info
        try:
            account = notifier.client.api.accounts(TWILIO_ACCOUNT_SID).fetch()
            print(f"   ✅ Account status: {account.status}")
        except Exception as e:
            print(f"   ❌ Error fetching account info: {e}")
    else:
        print("   ❌ Failed to initialize Twilio client")
        return
    
    # Send test message with detailed error handling
    print("\n4. Sending Test Message:")
    try:
        message = f"🧪 SMS Diagnostic Test\n\nTime: {datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}\n\nIf you receive this, SMS is working!"
        
        sms = notifier.client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=TARGET_PHONE_NUMBER
        )
        
        print(f"   ✅ Message sent successfully!")
        print(f"   📝 Message SID: {sms.sid}")
        print(f"   📝 Status: {sms.status}")
        print(f"   📝 Direction: {sms.direction}")
        
        # Check message status
        message_status = notifier.client.messages(sms.sid).fetch()
        print(f"   📝 Current Status: {message_status.status}")
        
        if message_status.error_code:
            print(f"   ❌ Error Code: {message_status.error_code}")
            print(f"   ❌ Error Message: {message_status.error_message}")
        
    except Exception as e:
        print(f"   ❌ Failed to send test message: {e}")
        return
    
    # Common troubleshooting tips
    print("\n5. Troubleshooting Tips:")
    print("   📋 If you're not receiving messages, check:")
    print("   • Check your spam/junk folder")
    print("   • Verify your phone can receive SMS from unknown numbers")
    print("   • Make sure your phone number is not blocked by your carrier")
    print("   • Try texting your Twilio number from your phone first")
    print("   • Check if your phone has any SMS blocking apps")
    print("   • Verify your carrier supports SMS from short codes/Twilio numbers")
    print(f"   • Try sending a test SMS to your Twilio number: {TWILIO_PHONE_NUMBER}")
    
    print("\n6. Next Steps:")
    print("   1. Wait 1-2 minutes for the test message to arrive")
    print("   2. If no message arrives, try texting 'START' to your Twilio number")
    print("   3. Check Twilio Console logs at https://console.twilio.com/")
    print("   4. Consider trying a different phone number to test")

if __name__ == "__main__":
    run_sms_diagnostics()