import customtkinter as ctk
from core.config import BADGES
from core.database import (
    get_profile, get_earned_badges, get_stages_explored, 
    get_myths_revealed, get_glossary_read_count, get_chatbot_questions_count,
    get_bookmarks, earn_badge, add_xp
)

class BadgeEngine:
    """Checks all badge conditions and awards badges with XP."""
    
    def check_all_badges(self) -> list[str]:
        """Returns list of newly earned badge_ids."""
        newly_earned = []
        profile = get_profile()
        earned = get_earned_badges()
        
        # first_step: any stage explored
        if "first_step" not in earned:
            if len(get_stages_explored()) >= 1:
                newly_earned.append("first_step")
        
        # bookworm: all 12 stages explored
        if "bookworm" not in earned:
            if len(get_stages_explored()) >= 12:
                newly_earned.append("bookworm")
        
        # myth_buster: all 18 myths revealed
        if "myth_buster" not in earned:
            if len(get_myths_revealed()) >= 18:
                newly_earned.append("myth_buster")
        
        # word_wizard: 25+ glossary terms read
        if "word_wizard" not in earned:
            if get_glossary_read_count() >= 25:
                newly_earned.append("word_wizard")
        
        # chatbot_friend: 10+ chatbot questions
        if "chatbot_friend" not in earned:
            if get_chatbot_questions_count() >= 10:
                newly_earned.append("chatbot_friend")
        
        # early_bird: simple check for new users
        if "early_bird" not in earned:
            newly_earned.append("early_bird")
            
        # fact_checker: 10+ bookmarks
        if "fact_checker" not in earned:
            if len(get_bookmarks()) >= 10:
                newly_earned.append("fact_checker")
        
        # Save all newly earned badges
        for badge_id in newly_earned:
            earn_badge(badge_id)
            badge_data = next((b for b in BADGES if b["id"] == badge_id), None)
            if badge_data:
                add_xp(badge_data["xp"])
        
        return newly_earned

badge_engine = BadgeEngine()
