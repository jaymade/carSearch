import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class EmailNotifier:
    def __init__(self, gmail_email=None, gmail_password=None, recipient_email=None):
        """
        Initialize email notifier using Gmail SMTP
        
        Args:
            gmail_email: Your Gmail address
            gmail_password: Your Gmail app password (not regular password)
            recipient_email: Email address to receive notifications
        """
        self.gmail_email = gmail_email
        self.gmail_password = gmail_password  
        self.recipient_email = recipient_email
        
    def send_vehicle_notification(self, vehicles: List[Dict]) -> bool:
        """Send email notification for new vehicles"""
        if not all([self.gmail_email, self.gmail_password, self.recipient_email]):
            logger.error("Email configuration incomplete")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"🚗 Honda Car Match Found - {len(vehicles)} Vehicle(s)"
            
            # Create HTML body
            html_body = """
            <html>
            <body>
            <h2>🎯 New Honda Match Found!</h2>
            """
            
            for i, vehicle in enumerate(vehicles, 1):
                html_body += f"""
                <div style="border: 1px solid #ccc; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h3>{vehicle.get('title', 'Unknown Vehicle')}</h3>
                """
                
                if 'price' in vehicle:
                    html_body += f"<p><strong>💰 Price:</strong> {vehicle['price']}</p>"
                
                if 'url' in vehicle:
                    html_body += f"<p><strong>🔗 Details:</strong> <a href='{vehicle['url']}'>View Vehicle</a></p>"
                
                if 'vin' in vehicle:
                    html_body += f"<p><strong>VIN:</strong> {vehicle['vin']}</p>"
                
                html_body += "</div>"
            
            html_body += f"""
            <p><strong>🕒 Search Time:</strong> {datetime.now().strftime('%m/%d/%Y %I:%M %p')}</p>
            <p><strong>📍 Dealership:</strong> AutoPark Honda</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_email, self.gmail_password)
            server.send_message(msg)
            server.quit()
            
            logger.info("Email notification sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
    
    def send_test_email(self) -> bool:
        """Send test email"""
        if not all([self.gmail_email, self.gmail_password, self.recipient_email]):
            logger.error("Email configuration incomplete")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.gmail_email
            msg['To'] = self.recipient_email
            msg['Subject'] = "🧪 Honda Car Search - Test Email"
            
            body = f"""
            <html>
            <body>
            <h2>🧪 Test Email Notification</h2>
            <p>This is a test to verify email notifications are working correctly.</p>
            <p><strong>Time:</strong> {datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}</p>
            <p>If you receive this email, notifications will work when vehicles are found!</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls() 
            server.login(self.gmail_email, self.gmail_password)
            server.send_message(msg)
            server.quit()
            
            logger.info("Test email sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send test email: {e}")
            return False