import json
import random
from core.database import save_quiz_result

class QuizEngine:
    def __init__(self, quiz_path="data/quiz_data.json"):
        with open(quiz_path, "r", encoding="utf-8") as f:
            self.all_questions = json.load(f)
            
    def get_quiz_session(self, category, limit=10):
        if category == "All":
            questions = random.sample(self.all_questions, min(limit, len(self.all_questions)))
        else:
            cat_qs = [q for q in self.all_questions if q['cat'] == category]
            questions = random.sample(cat_qs, min(limit, len(cat_qs)))
        return questions

    def process_result(self, category, score, total, time_taken):
        xp_per_correct = 10
        xp_earned = score * xp_per_correct
        if score == total: xp_earned += 50  # Bonus for perfect score
        
        badge = ""
        if score == total: badge = "perfect_score"
        
        save_quiz_result(category, score, total, xp_earned, badge, time_taken)
        return xp_earned, badge

quiz_engine = QuizEngine()
