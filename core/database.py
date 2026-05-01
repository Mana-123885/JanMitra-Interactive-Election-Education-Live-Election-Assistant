import sqlite3
import os
from datetime import datetime
from core.config import LEVELS

DB_PATH = "janmitra.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Profile table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY DEFAULT 1,
        name TEXT DEFAULT 'Voter',
        user_type TEXT DEFAULT 'General',
        language TEXT DEFAULT 'en',
        state TEXT DEFAULT '',
        district TEXT DEFAULT '',
        constituency TEXT DEFAULT '',
        age_group TEXT DEFAULT '',
        theme TEXT DEFAULT 'dark',
        font_size TEXT DEFAULT 'medium',
        onboarding_done INTEGER DEFAULT 0,
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0,
        last_active TEXT DEFAULT '',
        chatbot_questions_asked INTEGER DEFAULT 0,
        glossary_terms_read INTEGER DEFAULT 0,
        languages_used TEXT DEFAULT 'en'
    )''')
    
    # Initialize profile if not exists
    cursor.execute("SELECT COUNT(*) FROM profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO profile (id) VALUES (1)")

    # Quiz history
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        score INTEGER NOT NULL,
        total INTEGER NOT NULL,
        xp_earned INTEGER NOT NULL,
        badge_earned TEXT DEFAULT '',
        time_taken_seconds INTEGER DEFAULT 0,
        timestamp TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # Learning progress
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS learning_progress (
        stage_id INTEGER PRIMARY KEY,
        stage_name TEXT,
        explored INTEGER DEFAULT 0,
        mini_quiz_done INTEGER DEFAULT 0,
        timestamp TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # Election type progress
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS election_type_progress (
        type_id TEXT PRIMARY KEY,
        viewed INTEGER DEFAULT 0,
        timestamp TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # Myth progress
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS myth_progress (
        myth_id INTEGER PRIMARY KEY,
        revealed INTEGER DEFAULT 0,
        timestamp TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # Badges earned
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS badges_earned (
        badge_id TEXT PRIMARY KEY,
        earned_on TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # Bookmarks
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_type TEXT NOT NULL,
        item_id TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT,
        timestamp TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # Chat history
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT DEFAULT (datetime('now','localtime'))
    )''')

    # Glossary read
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS glossary_read (
        term TEXT PRIMARY KEY,
        timestamp TEXT DEFAULT (datetime('now','localtime'))
    )''')

    conn.commit()
    conn.close()

def get_profile():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {}

def update_profile(**kwargs):
    if not kwargs: return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    keys = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values())
    cursor.execute(f"UPDATE profile SET {keys} WHERE id = 1", values)
    conn.commit()
    conn.close()

def add_xp(amount):
    profile = get_profile()
    new_xp = profile['xp'] + amount
    update_profile(xp=new_xp)
    return new_xp

def get_level(xp):
    current_level = LEVELS[0]
    for level in LEVELS:
        if xp >= level['xp']:
            current_level = level
        else:
            break
    return current_level

def save_quiz_result(category, score, total, xp, badge, time_taken):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO quiz_history (category, score, total, xp_earned, badge_earned, time_taken_seconds)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (category, score, total, xp, badge, time_taken))
    conn.commit()
    conn.close()
    add_xp(xp)

def get_quiz_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz_history ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_best_score(category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(score) FROM quiz_history WHERE category = ?", (category,))
    score = cursor.fetchone()[0]
    conn.close()
    return score if score is not None else 0

def mark_stage_explored(stage_id, stage_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO learning_progress (stage_id, stage_name, explored) VALUES (?, ?, 1)", (stage_id, stage_name))
    conn.commit()
    conn.close()

def get_stages_explored():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT stage_id FROM learning_progress WHERE explored = 1")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def mark_myth_revealed(myth_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO myth_progress (myth_id, revealed) VALUES (?, 1)", (myth_id,))
    conn.commit()
    conn.close()

def get_myths_revealed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT myth_id FROM myth_progress WHERE revealed = 1")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def earn_badge(badge_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM badges_earned WHERE badge_id = ?", (badge_id,))
    exists = cursor.fetchone()[0]
    if exists == 0:
        cursor.execute("INSERT INTO badges_earned (badge_id) VALUES (?)", (badge_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def get_earned_badges():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT badge_id FROM badges_earned")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def add_bookmark(item_type, item_id, title, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookmarks (item_type, item_id, title, content) VALUES (?, ?, ?, ?)", (item_type, item_id, title, content))
    conn.commit()
    conn.close()

def get_bookmarks():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookmarks")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def remove_bookmark(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookmarks WHERE item_id = ?", (item_id,))
    conn.commit()
    conn.close()

def save_chat_message(role, message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (role, message) VALUES (?, ?)", (role, message))
    conn.commit()
    conn.close()

def get_chat_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_history ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def clear_chat_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history")
    conn.commit()
    conn.close()

def mark_glossary_read(term):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO glossary_read (term) VALUES (?)", (term,))
    conn.commit()
    conn.close()
    
    # Increment global count in profile
    profile = get_profile()
    update_profile(glossary_terms_read = profile['glossary_terms_read'] + 1)

def get_glossary_read_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM glossary_read")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def increment_chatbot_questions():
    profile = get_profile()
    update_profile(chatbot_questions_asked = profile['chatbot_questions_asked'] + 1)

def get_chatbot_questions_count():
    profile = get_profile()
    return profile['chatbot_questions_asked']

def reset_all_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Reset profile values
    cursor.execute('''
        UPDATE profile SET 
        onboarding_done = 0, 
        xp = 0, 
        streak = 0, 
        chatbot_questions_asked = 0, 
        glossary_terms_read = 0,
        last_active = '',
        languages_used = 'en'
        WHERE id = 1
    ''')
    
    # Clear all progress/history tables
    tables = [
        'quiz_history', 'learning_progress', 'election_type_progress',
        'myth_progress', 'badges_earned', 'bookmarks', 'chat_history', 'glossary_read'
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
        
    conn.commit()
    conn.close()

# Initialize DB on import
init_db()
