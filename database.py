import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict

DB_FILE = 'lemonbot.db'

class Database:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_file)
    
    def init_db(self):
        """Initialiser la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Table utilisateurs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                balance REAL DEFAULT 100,
                level INTEGER DEFAULT 1,
                exp INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table avis/reviews
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Table ferme (récoltes)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS farm (
                farm_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                lemon_count INTEGER DEFAULT 0,
                last_harvest TIMESTAMP,
                harvest_rate INTEGER DEFAULT 10,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Table items/shop
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item_name TEXT,
                quantity INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Table statistiques
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                lemons_harvested INTEGER DEFAULT 0,
                items_purchased INTEGER DEFAULT 0,
                total_spent REAL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id: int, username: str, first_name: str) -> bool:
        """Ajouter un nouvel utilisateur"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name)
                VALUES (?, ?, ?)
            ''', (user_id, username, first_name))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'utilisateur: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Récupérer les infos utilisateur"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            conn.close()
            if user:
                return {
                    'user_id': user[0],
                    'username': user[1],
                    'first_name': user[2],
                    'balance': user[3],
                    'level': user[4],
                    'exp': user[5],
                    'created_at': user[6],
                    'last_active': user[7]
                }
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération de l'utilisateur: {e}")
            return None
    
    def add_review(self, user_id: int, rating: int, comment: str) -> bool:
        """Ajouter un avis"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reviews (user_id, rating, comment)
                VALUES (?, ?, ?)
            ''', (user_id, rating, comment))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'avis: {e}")
            return False
    
    def get_reviews(self, limit: int = 10) -> List[Dict]:
        """Récupérer les avis"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.review_id, r.user_id, r.rating, r.comment, r.created_at, u.username
                FROM reviews r
                JOIN users u ON r.user_id = u.user_id
                ORDER BY r.created_at DESC
                LIMIT ?
            ''', (limit,))
            reviews = cursor.fetchall()
            conn.close()
            return [
                {
                    'review_id': r[0],
                    'user_id': r[1],
                    'rating': r[2],
                    'comment': r[3],
                    'created_at': r[4],
                    'username': r[5]
                }
                for r in reviews
            ]
        except Exception as e:
            print(f"Erreur lors de la récupération des avis: {e}")
            return []
    
    def update_balance(self, user_id: int, amount: float) -> bool:
        """Mettre à jour le solde"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET balance = balance + ? WHERE user_id = ?
            ''', (amount, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour du solde: {e}")
            return False
    
    def update_exp(self, user_id: int, exp: int) -> bool:
        """Mettre à jour l'expérience"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET exp = exp + ? WHERE user_id = ?
            ''', (exp, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'exp: {e}")
            return False

db = Database()
