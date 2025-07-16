import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Configuration class for the LeetCode WhatsApp Agent"""
    
    # Twilio WhatsApp API Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
    YOUR_WHATSAPP_NUMBER = os.getenv('YOUR_WHATSAPP_NUMBER', '')
    
    # Scheduling Configuration
    DAILY_SEND_TIME = os.getenv('DAILY_SEND_TIME', '09:00')
    TIMEZONE = os.getenv('TIMEZONE', 'America/New_York')
    
    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'leetcode_agent.db')
    
    # LeetCode Configuration
    LEETCODE_API_URL = 'https://leetcode.com/api/problems/all/'
    LEETCODE_GRAPHQL_URL = 'https://leetcode.com/graphql'
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        missing = []
        
        if not cls.TWILIO_ACCOUNT_SID:
            missing.append('TWILIO_ACCOUNT_SID')
        if not cls.TWILIO_AUTH_TOKEN:
            missing.append('TWILIO_AUTH_TOKEN')
        if not cls.YOUR_WHATSAPP_NUMBER:
            missing.append('YOUR_WHATSAPP_NUMBER')
            
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        return True 