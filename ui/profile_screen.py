import customtkinter as ctk
from core.config import COLORS, BADGES, LEVELS
from core.language import lang
from core.database import get_profile, get_earned_badges, get_level, get_quiz_history
from ui.components import make_section_header, make_badge_tile, make_level_badge

class ProfileScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        mode = ctk.get_appearance_mode()
        super().__init__(parent, fg_color=COLORS[mode]["bg"])
        self.nav = nav
        self.profile = get_profile()
        self.earned_badges = get_earned_badges()
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = make_section_header(self.scroll, lang.get("profile_title"), lang.get("profile_summary"))
        header.pack(fill="x", pady=(0, 20))
        
        # Profile Top Card
        top_card = ctk.CTkFrame(self.scroll, fg_color=COLORS[mode]["surface2"], corner_radius=20)
        top_card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(top_card, text="👤", font=("Arial", 64)).pack(side="left", padx=30, pady=30)
        
        info_frame = ctk.CTkFrame(top_card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=30)
        
        ctk.CTkLabel(info_frame, text=self.profile['name'], font=("Inter", 28, "bold"), anchor="w").pack(fill="x")
        ctk.CTkLabel(info_frame, text=f"Citizen ID: #JM-{self.profile['id']:04d}", font=("Inter", 14), text_color=COLORS[mode]["text3"], anchor="w").pack(fill="x")
        
        # Level Badge
        level = get_level(self.profile['xp'])
        next_lvl_xp = 2500 # Default for top level
        for l in LEVELS:
            if l['level'] == level['level'] + 1:
                next_lvl_xp = l['xp']
                break
        
        lvl_badge = make_level_badge(self.scroll, level, self.profile['xp'], next_lvl_xp)
        lvl_badge.pack(fill="x", pady=10)
        
        # Badges Section
        ctk.CTkLabel(self.scroll, text=lang.get("badges_label"), font=("Inter", 18, "bold")).pack(anchor="w", pady=(20, 10))
        
        badges_grid = ctk.CTkFrame(self.scroll, fg_color="transparent")
        badges_grid.pack(fill="x")
        
        cols = 5
        for i, badge in enumerate(BADGES):
            earned = badge['id'] in self.earned_badges
            tile = make_badge_tile(badges_grid, badge, earned)
            tile.grid(row=i // cols, column=i % cols, padx=10, pady=10, sticky="nsew")
            badges_grid.grid_columnconfigure(i % cols, weight=1)

        # Quiz History
        ctk.CTkLabel(self.scroll, text="Quiz History", font=("Inter", 18, "bold")).pack(anchor="w", pady=(20, 10))
        history = get_quiz_history()
        
        if not history:
            ctk.CTkLabel(self.scroll, text="No quizzes taken yet.", font=("Inter", 14, "italic"), text_color=COLORS[mode]["text3"]).pack(pady=10)
        else:
            for h in history[:5]: # Show last 5
                h_card = ctk.CTkFrame(self.scroll, fg_color=COLORS[mode]["surface3"], corner_radius=10)
                h_card.pack(fill="x", pady=5)
                ctk.CTkLabel(h_card, text=f"🎯 {h['category']} Quiz", font=("Inter", 14, "bold"), padx=15, pady=10).pack(side="left")
                ctk.CTkLabel(h_card, text=f"Score: {h['score']}/{h['total']} | +{h['xp_earned']} XP", font=("Inter", 13), padx=15).pack(side="right")
