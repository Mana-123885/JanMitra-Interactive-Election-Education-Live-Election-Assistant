import customtkinter as ctk
from core.config import COLORS, LEVELS
from core.language import lang
from core.database import get_profile, get_level, get_stages_explored, get_earned_badges
from ui.components import make_section_header, make_stat_chip, make_level_badge, make_card

class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        mode = ctk.get_appearance_mode()
        super().__init__(parent, fg_color=COLORS[mode]["bg"])
        self.nav = nav
        self.profile = get_profile()
        
        # Main scrollable area
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = make_section_header(self.scroll, lang.get("welcome_greeting", name=self.profile['name']), lang.get("tagline"))
        header.pack(fill="x", pady=(0, 20))
        
        # Stats Row
        stats_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        level = get_level(self.profile['xp'])
        next_lvl_xp = 5000 # Default
        for i, l in enumerate(LEVELS):
            if l['level'] == level['level'] + 1:
                next_lvl_xp = l['xp']
                break
        
        self.level_card = make_level_badge(stats_frame, level, self.profile['xp'], next_lvl_xp)
        self.level_card.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5)
        
        self.xp_chip = make_stat_chip(stats_frame, "✨", self.profile['xp'], "Total XP", COLORS[mode]["primary"])
        self.xp_chip.grid(row=0, column=2, sticky="nsew", padx=5)
        
        self.streak_chip = make_stat_chip(stats_frame, "🔥", self.profile['streak'], "Day Streak", COLORS[mode]["secondary"])
        self.streak_chip.grid(row=0, column=3, sticky="nsew", padx=5)
        
        # Quick Actions
        ctk.CTkLabel(self.scroll, text=lang.get("quick_actions"), font=("Inter", 18, "bold")).pack(anchor="w", pady=(20, 10))
        
        actions_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        actions_frame.pack(fill="x")
        actions_frame.grid_columnconfigure((0, 1), weight=1)
        
        from ui.learn import LearnScreen
        from ui.quiz_screen import QuizScreen
        from ui.chatbot_screen import ChatbotScreen
        from ui.myth_fact import MythFactScreen
        
        learn_card = make_card(actions_frame, lang.get("nav_learn"), "Master the 12 stages of Indian elections", "📚", COLORS[mode]["primary"], 
                               on_click=lambda: self.nav.switch_screen(LearnScreen))
        learn_card.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        quiz_card = make_card(actions_frame, lang.get("nav_quiz"), "Test your civic knowledge and earn XP", "🎯", COLORS[mode]["secondary"], 
                              on_click=lambda: self.nav.switch_screen(QuizScreen))
        quiz_card.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        chat_card = make_card(actions_frame, lang.get("nav_chatbot"), "Ask any question about the democratic process", "🤖", COLORS[mode]["accent"], 
                               on_click=lambda: self.nav.switch_screen(ChatbotScreen))
        chat_card.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        myth_card = make_card(actions_frame, lang.get("nav_myths"), "Debunk common election misconceptions", "💥", COLORS[mode]["error"], 
                              on_click=lambda: self.nav.switch_screen(MythFactScreen))
        myth_card.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Today's Fact
        ctk.CTkLabel(self.scroll, text=lang.get("today_fact"), font=("Inter", 18, "bold")).pack(anchor="w", pady=(20, 10))
        fact_card = ctk.CTkFrame(self.scroll, fg_color=COLORS[mode]["surface3"], corner_radius=15)
        fact_card.pack(fill="x", pady=5)
        
        fact_text = "The voting age in India was reduced from 21 to 18 by the 61st Constitutional Amendment Act, 1988."
        ctk.CTkLabel(fact_card, text=fact_text, font=("Inter", 14, "italic"), wraplength=700, pady=20, padx=20).pack()
