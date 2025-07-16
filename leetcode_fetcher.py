import requests
import json
import time
import random
from typing import List, Dict, Optional
from database import LeetCodeDatabase
from config import Config

class LeetCodeFetcher:
    """Fetches LeetCode problems and manages problem selection"""
    
    def __init__(self):
        self.db = LeetCodeDatabase()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_all_problems(self) -> bool:
        """Fetch all problems from LeetCode and store in database"""
        try:
            print("Fetching LeetCode problems...")
            
            # GraphQL query to get all problems
            query = """
            {
                allQuestions {
                    title
                    titleSlug
                    difficulty
                    questionId
                    isPaidOnly
                }
            }
            """
            
            response = self.session.post(
                Config.LEETCODE_GRAPHQL_URL,
                json={'query': query},
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Failed to fetch problems: {response.status_code}")
                return False
            
            data = response.json()
            problems = data.get('data', {}).get('allQuestions', [])
            
            if not problems:
                print("No problems found in response")
                return False
            
            # Filter out paid-only problems and add to database
            added_count = 0
            for problem in problems:
                if not problem.get('isPaidOnly', True):  # Only free problems
                    leetcode_id = int(problem['questionId'])
                    title = problem['title']
                    difficulty = problem['difficulty']
                    url = f"https://leetcode.com/problems/{problem['titleSlug']}/"
                    
                    if self.db.add_problem(leetcode_id, title, difficulty, url):
                        added_count += 1
            
            print(f"Successfully added {added_count} problems to database")
            return True
            
        except Exception as e:
            print(f"Error fetching problems: {e}")
            return False
    
    def get_daily_problems(self) -> Optional[Dict[str, Dict]]:
        """Get one easy, medium, and hard problem for today"""
        today = time.strftime('%Y-%m-%d')
        
        # Check if we already sent problems today
        if self.db.was_batch_sent_today(today):
            print("Problems already sent today")
            return None
        
        # Get one problem of each difficulty
        easy_problem = self.db.get_unsent_problem('Easy')
        medium_problem = self.db.get_unsent_problem('Medium')
        hard_problem = self.db.get_unsent_problem('Hard')
        
        # Check if we have problems of all difficulties
        if not all([easy_problem, medium_problem, hard_problem]):
            missing = []
            if not easy_problem:
                missing.append('Easy')
            if not medium_problem:
                missing.append('Medium')
            if not hard_problem:
                missing.append('Hard')
            
            print(f"Missing problems for difficulties: {', '.join(missing)}")
            
            # Try to fetch more problems if we're running low
            if not self.fetch_all_problems():
                return None
            
            # Try again after fetching
            if not easy_problem:
                easy_problem = self.db.get_unsent_problem('Easy')
            if not medium_problem:
                medium_problem = self.db.get_unsent_problem('Medium')
            if not hard_problem:
                hard_problem = self.db.get_unsent_problem('Hard')
            
            if not all([easy_problem, medium_problem, hard_problem]):
                print("Still missing problems after fetch attempt")
                return None
        
        # Mark problems as sent and record the batch
        self.db.mark_problem_sent(easy_problem['id'], 'Easy', today)
        self.db.mark_problem_sent(medium_problem['id'], 'Medium', today)
        self.db.mark_problem_sent(hard_problem['id'], 'Hard', today)
        
        self.db.record_daily_batch(
            today,
            easy_problem['id'],
            medium_problem['id'],
            hard_problem['id']
        )
        
        return {
            'easy': easy_problem,
            'medium': medium_problem,
            'hard': hard_problem
        }
    
    def format_problems_message(self, problems: Dict[str, Dict]) -> str:
        """Format the problems into a WhatsApp message"""
        message_parts = [
            "🚀 *Daily LeetCode Challenge!* 🚀",
            "",
            "Here are your 3 problems for today:",
            ""
        ]
        
        difficulty_emojis = {
            'easy': '🟢',
            'medium': '🟡',
            'hard': '🔴'
        }
        
        for difficulty, problem in problems.items():
            emoji = difficulty_emojis.get(difficulty, '⚪')
            title = problem['title']
            url = problem['url']
            
            message_parts.extend([
                f"{emoji} *{difficulty.upper()}*: {title}",
                f"🔗 {url}",
                ""
            ])
        
        message_parts.extend([
            "Good luck and happy coding! 💪",
            "",
            "Remember:",
            "• Read the problem carefully",
            "• Think about edge cases",
            "• Optimize your solution",
            "• Test with examples"
        ])
        
        return "\n".join(message_parts)
    
    def get_problem_stats(self) -> str:
        """Get statistics about problems in database"""
        total_counts = self.db.get_problem_count_by_difficulty()
        sent_counts = self.db.get_sent_count_by_difficulty()
        
        stats = ["📊 *Problem Statistics*", ""]
        
        for difficulty in ['Easy', 'Medium', 'Hard']:
            total = total_counts.get(difficulty, 0)
            sent = sent_counts.get(difficulty, 0)
            remaining = total - sent
            
            stats.append(f"{difficulty}: {remaining}/{total} remaining")
        
        return "\n".join(stats) 