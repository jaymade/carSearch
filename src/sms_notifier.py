import logging
from datetime import datetime
from typing import List, Dict, Optional
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, TARGET_PHONE_NUMBER

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Twilio not installed. Install with: pip install twilio")

logger = logging.getLogger(__name__)

class SMSNotifier:
    def __init__(self):
        self.client = None
        self.setup_twilio()
    
    def setup_twilio(self) -> bool:
        """Initialize Twilio client"""
        try:
            if not TWILIO_AVAILABLE:
                logger.error("Twilio is not installed. Please run: pip install twilio")
                return False
                
            if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
                logger.error("Missing Twilio configuration. Please check your .env file.")
                return False
            
            self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            logger.info("Twilio client initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Twilio client: {e}")
            return False
    
    def format_vehicle_message(self, vehicle: Dict) -> str:
        """Format vehicle information into SMS message"""
        message_parts = []
        
        # Title/name
        if 'title' in vehicle:
            message_parts.append(f"🚗 {vehicle['title']}")
        
        # Price
        if 'price' in vehicle:
            message_parts.append(f"💰 {vehicle['price']}")
        
        # VIN if available (helps identify specific vehicle)
        if 'vin' in vehicle:
            message_parts.append(f"� VIN: {vehicle['vin']}")
        
        # Direct link to view the vehicle
        if 'url' in vehicle:
            message_parts.append(f"👀 VIEW CAR: {vehicle['url']}")
        
        return "\n".join(message_parts)
    
    def send_notification(self, vehicles: List[Dict]) -> bool:
        """Send SMS notification for new vehicles"""
        if not self.client:
            logger.error("Twilio client not initialized")
            return False
        
        if not vehicles:
            logger.info("No vehicles to notify about")
            return True
        
        try:
            # Create message content
            if len(vehicles) == 1:
                message = f"🎯 NEW HONDA MATCH FOUND!\n\n{self.format_vehicle_message(vehicles[0])}"
            else:
                message = f"🎯 {len(vehicles)} NEW HONDA MATCHES!\n\n"
                for i, vehicle in enumerate(vehicles[:2], 1):  # Limit to 2 for SMS space
                    message += f"#{i} {vehicle.get('title', 'Honda Vehicle')}\n"
                    if 'price' in vehicle:
                        message += f"💰 {vehicle['price']}\n"
                    if 'url' in vehicle:
                        message += f"👀 {vehicle['url']}\n"
                    message += "\n"
                
                if len(vehicles) > 2:
                    message += f"+ {len(vehicles) - 2} more matches!\n"
                
                # Add search links
                message += "🔍 Quick Links:\n"
                message += "New: autoparkhonda.com/new-inventory/\n"
                message += "Used: autoparkhonda.com/used-inventory/"
            
            # Add timestamp and source
            message += f"\n🕒 {datetime.now().strftime('%m/%d %I:%M%p')}"
            message += f"\n📍 AutoPark Honda - Cary, NC"
            
            # Send SMS
            sms = self.client.messages.create(
                body=message[:1500],  # SMS character limit
                from_=TWILIO_PHONE_NUMBER,
                to=TARGET_PHONE_NUMBER
            )
            
            logger.info(f"SMS sent successfully. SID: {sms.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")
            return False
    
    def send_test_message(self) -> bool:
        """Send a test message to verify SMS functionality"""
        if not self.client:
            logger.error("Twilio client not initialized")
            return False
        
        try:
            message = "🧪 Honda Car Search App - Test Message\n\nThis is a test to verify SMS notifications are working correctly."
            
            sms = self.client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=TARGET_PHONE_NUMBER
            )
            
            logger.info(f"Test SMS sent successfully. SID: {sms.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send test SMS: {e}")
            return False
    
    def send_error_notification(self, error_message: str) -> bool:
        """Send error notification SMS"""
        if not self.client:
            return False
        
        try:
            message = f"⚠️ Honda Car Search Error\n\n{error_message}\n\n🕒 {datetime.now().strftime('%m/%d/%Y %I:%M %p')}"
            
            sms = self.client.messages.create(
                body=message[:1500],
                from_=TWILIO_PHONE_NUMBER,
                to=TARGET_PHONE_NUMBER
            )
            
            logger.info(f"Error notification SMS sent. SID: {sms.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send error SMS: {e}")
            return False
    
    def generate_search_link(self) -> str:
        """Generate a direct link to search results on the dealership website"""
        # Create a cleaner search URL for users to bookmark/use
        base_url = "https://www.autoparkhonda.com/new-inventory/"
        params = "?make=Honda&model=Civic&model=Civic%20Hybrid&trim=Sport&trim=Sport%20Touring"
        return base_url + params
    
    def send_no_matches_notification(self) -> bool:
        """Send notification when no vehicles match the criteria"""
        if not self.client:
            logger.error("Twilio client not initialized")
            return False
        
        try:
            search_link = self.generate_search_link()
            message = (
                "🔍 Honda Search - No New Matches\n\n"
                "No NEW Honda Civic/Civic Hybrid vehicles found matching:\n"
                "• Sport/Sport Touring trim\n"
                "• Black Sedan\n\n"
                f"🔗 Check all inventory: {search_link}\n\n"
                "Next search in a few hours...\n"
                f"🕒 {datetime.now().strftime('%m/%d %I:%M%p')}"
            )
            
            sms = self.client.messages.create(
                body=message[:1500],
                from_=TWILIO_PHONE_NUMBER,
                to=TARGET_PHONE_NUMBER
            )
            
            logger.info(f"No matches notification SMS sent. SID: {sms.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send no matches SMS: {e}")
            return False