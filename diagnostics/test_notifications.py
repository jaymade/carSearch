#!/usr/bin/env python3
"""
Test script that sends a test notification with sample vehicle data
"""

import sys
import os

# Add src directory to path  
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from sms_notifier import SMSNotifier

def test_notification():
    """Test SMS notification with sample vehicle data"""
    
    # Create sample vehicle data with real-looking links
    sample_vehicles = [
        {
            'title': '2026 Honda Civic Sport Sedan',
            'price': '$27,790',
            'url': 'https://www.autoparkhonda.com/new/Honda/2026-Honda-Civic-bbeeb5b1ac1819737b2830bb6d2999b1.htm',
            'vin': '2HGFE2F58TH526131',
            'year': '2026',
            'make': 'Honda', 
            'model': 'Civic Sport'
        },
        {
            'title': '2026 Honda Civic Hybrid Sport Touring',
            'price': '$33,490',
            'url': 'https://www.autoparkhonda.com/new/Honda/2026-Honda-Civic-Hybrid-1315c803ac1805c330b79c996173661a.htm',
            'vin': '2HGFE4F87TH308445',
            'year': '2026',
            'make': 'Honda',
            'model': 'Civic Hybrid Sport Touring'
        },
        {
            'title': '2025 Honda Civic Hybrid Sport',
            'price': '$31,290',
            'url': 'https://www.autoparkhonda.com/new/Honda/2025-Honda-Civic-Hybrid-a87eb8b9ac183d310e10b67dc1d14d75.htm',
            'vin': '2HGFE4F52TH298766',
            'year': '2025',
            'make': 'Honda',
            'model': 'Civic Hybrid Sport'
        }
    ]
    
    print("📱 Testing SMS Notification System")
    print("=" * 50)
    
    notifier = SMSNotifier()
    
    print("\n1. Testing with single vehicle:")
    success1 = notifier.send_notification([sample_vehicles[0]])
    print(f"   Result: {'✅ Success' if success1 else '❌ Failed'}")
    
    print("\n2. Testing with multiple vehicles:")
    success2 = notifier.send_notification(sample_vehicles)
    print(f"   Result: {'✅ Success' if success2 else '❌ Failed'}")
    
    print("\n3. Testing 'no matches' notification:")
    success3 = notifier.send_no_matches_notification()
    print(f"   Result: {'✅ Success' if success3 else '❌ Failed'}")
    
    if success1 or success2:
        print("\n🎉 SMS notifications are working!")
        print("   When real vehicles are found, you'll receive notifications like these.")
    else:
        print("\n❌ SMS notifications failed.")
        print("   Check your Twilio credentials in the .env file.")

if __name__ == "__main__":
    test_notification()