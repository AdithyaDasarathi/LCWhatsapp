#!/usr/bin/env python3
"""
LeetCode WhatsApp Agent

A daily agent that sends one easy, medium, and hard LeetCode problem 
via WhatsApp using Twilio API.
"""

import time
import sys
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from config import Config
from leetcode_fetcher import LeetCodeFetcher
from whatsapp_sender import WhatsAppSender
from database import LeetCodeDatabase

class LeetCodeAgent:
    """Main agent that coordinates LeetCode problem delivery"""
    
    def __init__(self):
        """Initialize the agent with all components"""
        print("🤖 Initializing LeetCode WhatsApp Agent...")
        
        self.leetcode_fetcher = LeetCodeFetcher()
        self.whatsapp_sender = WhatsAppSender()
        self.db = LeetCodeDatabase()
        
        # Set up timezone
        self.timezone = pytz.timezone(Config.TIMEZONE)
        
        # Parse the daily send time
        self.send_hour, self.send_minute = map(int, Config.DAILY_SEND_TIME.split(':'))
        
        print(f"📅 Scheduled to send daily at {Config.DAILY_SEND_TIME} {Config.TIMEZONE}")
        print("✅ Agent initialized successfully!")
    
    def send_daily_problems(self):
        """Main function to send daily problems"""
        print(f"\n🔄 Starting daily problem send at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check if WhatsApp is configured
        if not self.whatsapp_sender.is_configured():
            print("❌ WhatsApp not configured. Please set up your Twilio credentials.")
            return False
        
        try:
            # Get today's problems
            problems = self.leetcode_fetcher.get_daily_problems()
            
            if not problems:
                print("⚠️ No problems available or already sent today")
                return False
            
            # Format the message
            formatted_message = self.leetcode_fetcher.format_problems_message(problems)
            
            # Send via WhatsApp
            success = self.whatsapp_sender.send_daily_problems(formatted_message)
            
            if success:
                print("✅ Daily problems sent successfully!")
                print(f"📊 Sent problems:")
                for difficulty, problem in problems.items():
                    print(f"   {difficulty.title()}: {problem['title']}")
                return True
            else:
                print("❌ Failed to send daily problems")
                return False
                
        except Exception as e:
            print(f"❌ Error in send_daily_problems: {e}")
            return False
    
    def send_stats(self):
        """Send problem statistics"""
        if not self.whatsapp_sender.is_configured():
            print("❌ WhatsApp not configured")
            return False
        
        stats_message = self.leetcode_fetcher.get_problem_stats()
        return self.whatsapp_sender.send_stats(stats_message)
    
    def test_setup(self):
        """Test the complete setup"""
        print("\n🧪 Testing agent setup...")
        
        # Test WhatsApp connection
        print("1. Testing WhatsApp connection...")
        if self.whatsapp_sender.test_connection():
            print("   ✅ WhatsApp connection successful")
        else:
            print("   ❌ WhatsApp connection failed")
            return False
        
        # Test LeetCode fetching
        print("2. Testing LeetCode problem fetching...")
        if self.leetcode_fetcher.fetch_all_problems():
            print("   ✅ LeetCode fetching successful")
        else:
            print("   ❌ LeetCode fetching failed")
            return False
        
        # Test database
        print("3. Testing database...")
        stats = self.leetcode_fetcher.get_problem_stats()
        print(f"   ✅ Database working. {stats}")
        
        print("\n✅ All tests passed! Agent is ready to run.")
        return True
    
    def run_once(self):
        """Run the agent once (for testing)"""
        print("🔄 Running agent once...")
        return self.send_daily_problems()
    
    def start_scheduler(self):
        """Start the scheduled agent"""
        print(f"\n🚀 Starting LeetCode WhatsApp Agent scheduler...")
        print(f"📅 Will send problems daily at {Config.DAILY_SEND_TIME} {Config.TIMEZONE}")
        print("🛑 Press Ctrl+C to stop the agent\n")
        
        scheduler = BlockingScheduler(timezone=self.timezone)
        
        # Schedule daily problems
        scheduler.add_job(
            func=self.send_daily_problems,
            trigger=CronTrigger(
                hour=self.send_hour,
                minute=self.send_minute,
                timezone=self.timezone
            ),
            id='daily_problems',
            name='Send Daily LeetCode Problems',
            misfire_grace_time=300  # 5 minutes grace time
        )
        
        try:
            print("📊 Scheduled jobs:")
            for job in scheduler.get_jobs():
                print(f"   • {job.name}: Next run scheduled")
            print()
            
            scheduler.start()
        except KeyboardInterrupt:
            print("\n👋 Agent stopped by user")
            try:
                scheduler.shutdown()
            except:
                pass
        except Exception as e:
            print(f"\n❌ Scheduler error: {e}")
            try:
                scheduler.shutdown()
            except:
                pass

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='LeetCode WhatsApp Agent')
    parser.add_argument('--test', action='store_true', help='Test the setup')
    parser.add_argument('--once', action='store_true', help='Run once (send problems now)')
    parser.add_argument('--stats', action='store_true', help='Send problem statistics')
    parser.add_argument('--fetch', action='store_true', help='Fetch all problems from LeetCode')
    
    args = parser.parse_args()
    
    agent = LeetCodeAgent()
    
    if args.test:
        agent.test_setup()
    elif args.once:
        agent.run_once()
    elif args.stats:
        agent.send_stats()
    elif args.fetch:
        if agent.leetcode_fetcher.fetch_all_problems():
            print("✅ Successfully fetched all problems")
        else:
            print("❌ Failed to fetch problems")
    else:
        # Default: start the scheduler
        agent.start_scheduler()

if __name__ == "__main__":
    main() 