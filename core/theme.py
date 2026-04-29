import customtkinter as ctk
from core.database import update_profile, get_profile

class ThemeManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
        return cls._instance
    
    def set_theme(self, mode):
        """mode: 'light' or 'dark'"""
        ctk.set_appearance_mode(mode)
        update_profile(theme=mode)
        
    def get_current_theme(self):
        profile = get_profile()
        return profile.get('theme', 'dark')

theme_manager = ThemeManager()
