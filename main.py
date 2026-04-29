import customtkinter as ctk
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import COLORS, APP_NAME
from core.database import get_profile
from core.theme import theme_manager
from core.language import lang
from core.navigation import NavigationManager

from ui.splash import SplashScreen
from ui.home import HomeScreen
from ui.learn import LearnScreen
from ui.election_types import ElectionTypesScreen
from ui.chatbot_screen import ChatbotScreen
from ui.quiz_screen import QuizScreen
from ui.myth_fact import MythFactScreen
from ui.glossary_screen import GlossaryScreen
from ui.live_updates import LiveUpdatesScreen
from ui.profile_screen import ProfileScreen
from ui.settings_screen import SettingsScreen
from ui.polling_simulator import PollingSimulatorScreen
from ui.components import make_nav_button

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Load theme from DB
        profile = get_profile()
        theme_manager.set_theme(profile.get('theme', 'dark'))
        lang.set_language(profile.get('language', 'en'))
        
        self.title(APP_NAME)
        self.geometry("1100x750")
        self.configure(fg_color=COLORS[ctk.get_appearance_mode()]["bg"])
        
        self.nav = NavigationManager(self)
        
        # Sidebar (Initially hidden for splash/onboarding)
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=COLORS[ctk.get_appearance_mode()]["surface"])
        self.nav.set_sidebar(self)
        
        self.nav_btns = {}
        self.create_sidebar_content()
        
        # Start with Splash
        self.nav.switch_screen(SplashScreen)
        
    def create_sidebar_content(self):
        mode = ctk.get_appearance_mode()
        
        # App Logo/Name
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", pady=30, padx=20)
        ctk.CTkLabel(logo_frame, text="🗳️", font=("Arial", 36)).pack(side="left")
        ctk.CTkLabel(logo_frame, text=APP_NAME, font=("Inter", 24, "bold"), text_color=COLORS[mode]["primary"]).pack(side="left", padx=10)
        
        # Nav Buttons
        self.add_nav_item("home", "🏠", lang.get("nav_home"), HomeScreen)
        self.add_nav_item("learn", "📚", lang.get("nav_learn"), LearnScreen)
        self.add_nav_item("types", "🏰", lang.get("nav_types"), ElectionTypesScreen)
        self.add_nav_item("quiz", "🎯", lang.get("nav_quiz"), QuizScreen)
        self.add_nav_item("simulator", "🗳️", "Polling Simulator", PollingSimulatorScreen)
        self.add_nav_item("chat", "🤖", lang.get("nav_chatbot"), ChatbotScreen)
        self.add_nav_item("live", "📈", lang.get("nav_live"), LiveUpdatesScreen)
        self.add_nav_item("myths", "💥", lang.get("nav_myths"), MythFactScreen)
        self.add_nav_item("glossary", "📖", lang.get("nav_glossary"), GlossaryScreen)
        
        # Bottom spacer
        ctk.CTkLabel(self.sidebar, text="", height=1).pack(fill="y", expand=True)
        
        self.add_nav_item("profile", "👤", lang.get("nav_profile"), ProfileScreen)
        self.add_nav_item("settings", "⚙️", lang.get("nav_settings"), SettingsScreen)
        
    def add_nav_item(self, id, emoji, label, screen_class):
        btn = make_nav_button(self.sidebar, emoji, label, False, lambda: self.nav.switch_screen(screen_class))
        btn.pack(fill="x", padx=15, pady=2)
        self.nav_btns[id] = btn

    def set_active(self, nav_id):
        for id, btn in self.nav_btns.items():
            is_active = (id == nav_id)
            mode = ctk.get_appearance_mode()
            bg = COLORS[mode]["primary"] if is_active else "transparent"
            fg = COLORS[mode]["text1"] if is_active else COLORS[mode]["text2"]
            btn.configure(fg_color=bg, text_color=fg)

    def show_sidebar(self):
        # Refresh sidebar text if language changed
        for widget in self.sidebar.winfo_children(): widget.destroy()
        self.create_sidebar_content()
        self.sidebar.pack(side="left", fill="y")

    def hide_sidebar(self):
        self.sidebar.pack_forget()

# Override switch_screen in NavigationManager to handle sidebar visibility
def patched_switch(self, screen_class, *args, **kwargs):
    if self.current_frame:
        self.current_frame.destroy()
    
    # Hide sidebar for splash and onboarding
    if screen_class in [SplashScreen, "OnboardingScreen"]: # Simplified check
        self.root.hide_sidebar()
    else:
        # Check if onboarding screen by name because of circular imports
        if screen_class.__name__ == "OnboardingScreen":
            self.root.hide_sidebar()
        else:
            self.root.show_sidebar()
            
    self.current_frame = screen_class(self.root, self, *args, **kwargs)
    self.current_frame.pack(side="right", fill="both", expand=True)
    
NavigationManager.switch_screen = patched_switch

if __name__ == "__main__":
    app = App()
    app.mainloop()
