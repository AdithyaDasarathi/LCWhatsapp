from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from typing import Optional
from config import Config

class WhatsAppSender:
    """Handles sending messages via WhatsApp using Twilio API"""
    
    def __init__(self):
        """Initialize Twilio client with configuration"""
        try:
            Config.validate_config()
            self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
            self.from_number = Config.TWILIO_WHATSAPP_FROM
            self.to_number = Config.YOUR_WHATSAPP_NUMBER
            print("WhatsApp sender initialized successfully")
        except ValueError as e:
            print(f"Configuration error: {e}")
            self.client = None
        except Exception as e:
            print(f"Failed to initialize WhatsApp sender: {e}")
            self.client = None
    
    def send_message(self, message: str) -> bool:
        """Send a message via WhatsApp"""
        if not self.client:
            print("WhatsApp client not initialized")
            return False
        
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )
            
            print(f"Message sent successfully. SID: {message_obj.sid}")
            return True
            
        except TwilioException as e:
            print(f"Twilio error sending message: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error sending message: {e}")
            return False
    
    def send_daily_problems(self, formatted_message: str) -> bool:
        """Send the daily LeetCode problems"""
        print("Sending daily LeetCode problems...")
        return self.send_message(formatted_message)
    
    def send_stats(self, stats_message: str) -> bool:
        """Send problem statistics"""
        print("Sending problem statistics...")
        return self.send_message(stats_message)
    
    def test_connection(self) -> bool:
        """Test the WhatsApp connection with a simple message"""
        if not self.client:
            return False
        
        test_message = "🤖 LeetCode WhatsApp Agent is online and ready!"
        return self.send_message(test_message)
    
    def is_configured(self) -> bool:
        """Check if WhatsApp is properly configured"""
        return self.client is not None 