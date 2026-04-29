import customtkinter as ctk
import json
from core.config import COLORS
from core.language import lang
from core.database import get_myths_revealed, mark_myth_revealed, add_xp
from ui.components import make_section_header, show_xp_toast

class MythFactScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        mode = ctk.get_appearance_mode()
        super().__init__(parent, fg_color=COLORS[mode]["bg"])
        self.nav = nav
        
        with open("data/myths_facts.json", "r", encoding="utf-8") as f:
            self.myths = json.load(f)
            
        self.revealed = get_myths_revealed()
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = make_section_header(self.scroll, lang.get("myth_title"), "Separate rumors from the truth")
        header.pack(fill="x", pady=(0, 20))
        
        self.render_myths()
        
    def render_myths(self):
        for myth in self.myths:
            is_revealed = myth['id'] in self.revealed
            
            card = ctk.CTkFrame(self.scroll, fg_color=COLORS[ctk.get_appearance_mode()]["surface2"], corner_radius=15, border_width=1, border_color=COLORS[ctk.get_appearance_mode()]["border"])
            card.pack(fill="x", pady=10)
            
            ctk.CTkLabel(card, text="🛑 Myth", font=("Inter", 14, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["error"]).pack(anchor="w", padx=20, pady=(15, 5))
            ctk.CTkLabel(card, text=myth['myth'], font=("Inter", 16, "bold"), wraplength=600, justify="left").pack(anchor="w", padx=20, pady=(0, 15))
            
            if is_revealed:
                self.show_fact(card, myth)
            else:
                btn = ctk.CTkButton(card, text=lang.get("myth_reveal"), font=("Inter", 14, "bold"), fg_color=COLORS[ctk.get_appearance_mode()]["primary"], 
                                    command=lambda c=card, m=myth: self.reveal_truth(c, m))
                btn.pack(pady=(0, 20))
                
    def reveal_truth(self, card, myth):
        for widget in card.winfo_children():
            if isinstance(widget, ctk.CTkButton): widget.destroy()
            
        mark_myth_revealed(myth['id'])
        add_xp(myth['xp_reward'])
        show_xp_toast(self, myth['xp_reward'], lang.get("myth_busted"))
        self.show_fact(card, myth)
        
        from services.badge_engine import badge_engine
        badge_engine.check_all_badges()
        
    def show_fact(self, card, myth):
        ctk.CTkLabel(card, text="✅ Fact", font=("Inter", 14, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["success"]).pack(anchor="w", padx=20, pady=(0, 5))
        ctk.CTkLabel(card, text=myth['fact'], font=("Inter", 14), wraplength=600, justify="left", text_color=COLORS[ctk.get_appearance_mode()]["text2"]).pack(anchor="w", padx=20, pady=(0, 20))
