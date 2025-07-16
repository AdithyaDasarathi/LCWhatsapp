import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from config import Config

class LeetCodeDatabase:
    """Database manager for tracking sent LeetCode problems"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create problems table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS problems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    leetcode_id INTEGER UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    url TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create sent_problems table to track what's been sent
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sent_problems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    problem_id INTEGER NOT NULL,
                    sent_date DATE NOT NULL,
                    difficulty TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (problem_id) REFERENCES problems (id)
                )
            ''')
            
            # Create daily_batches table to track complete daily sends
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_batches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE UNIQUE NOT NULL,
                    easy_problem_id INTEGER,
                    medium_problem_id INTEGER,
                    hard_problem_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (easy_problem_id) REFERENCES problems (id),
                    FOREIGN KEY (medium_problem_id) REFERENCES problems (id),
                    FOREIGN KEY (hard_problem_id) REFERENCES problems (id)
                )
            ''')
            
            conn.commit()
    
    def add_problem(self, leetcode_id: int, title: str, difficulty: str, url: str) -> int:
        """Add a new problem to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO problems (leetcode_id, title, difficulty, url)
                    VALUES (?, ?, ?, ?)
                ''', (leetcode_id, title, difficulty, url))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # Problem already exists, return existing ID
                cursor.execute('SELECT id FROM problems WHERE leetcode_id = ?', (leetcode_id,))
                result = cursor.fetchone()
                return result[0] if result else None
    
    def get_unsent_problem(self, difficulty: str) -> Optional[Dict]:
        """Get a random unsent problem of specified difficulty"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, p.leetcode_id, p.title, p.difficulty, p.url
                FROM problems p
                LEFT JOIN sent_problems sp ON p.id = sp.problem_id
                WHERE p.difficulty = ? AND sp.id IS NULL
                ORDER BY RANDOM()
                LIMIT 1
            ''', (difficulty,))
            
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'leetcode_id': result[1],
                    'title': result[2],
                    'difficulty': result[3],
                    'url': result[4]
                }
            return None
    
    def mark_problem_sent(self, problem_id: int, difficulty: str, date: str = None):
        """Mark a problem as sent"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sent_problems (problem_id, sent_date, difficulty)
                VALUES (?, ?, ?)
            ''', (problem_id, date, difficulty))
            conn.commit()
    
    def record_daily_batch(self, date: str, easy_id: int, medium_id: int, hard_id: int):
        """Record a complete daily batch of problems"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO daily_batches 
                (date, easy_problem_id, medium_problem_id, hard_problem_id)
                VALUES (?, ?, ?, ?)
            ''', (date, easy_id, medium_id, hard_id))
            conn.commit()
    
    def was_batch_sent_today(self, date: str = None) -> bool:
        """Check if a batch was already sent today"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM daily_batches WHERE date = ?', (date,))
            return cursor.fetchone() is not None
    
    def get_problem_count_by_difficulty(self) -> Dict[str, int]:
        """Get count of problems by difficulty"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT difficulty, COUNT(*) 
                FROM problems 
                GROUP BY difficulty
            ''')
            
            return dict(cursor.fetchall())
    
    def get_sent_count_by_difficulty(self) -> Dict[str, int]:
        """Get count of sent problems by difficulty"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT difficulty, COUNT(*) 
                FROM sent_problems 
                GROUP BY difficulty
            ''')
            
            return dict(cursor.fetchall()) 