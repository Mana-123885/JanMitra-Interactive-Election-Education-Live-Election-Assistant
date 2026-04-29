import customtkinter as ctk
import json
from core.config import COLORS
from core.language import lang
from core.database import get_stages_explored, mark_stage_explored, add_xp
from ui.components import make_section_header, make_card, show_xp_toast

class LearnScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        mode = ctk.get_appearance_mode()
        super().__init__(parent, fg_color=COLORS[mode]["bg"])
        self.nav = nav
        
        with open("data/election_content.json", "r", encoding="utf-8") as f:
            self.stages = json.load(f)
            
        self.explored = get_stages_explored()
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = make_section_header(self.scroll, lang.get("learn_title"), lang.get("learn_subtitle"))
        header.pack(fill="x", pady=(0, 20))
        
        self.stage_frames = []
        self.render_stages()
        
    def render_stages(self):
        for stage in self.stages:
            is_done = stage['stage_id'] in self.explored
            status_text = lang.get("stage_done") if is_done else f"{stage['xp_reward']} XP"
            color = stage['color'] if not is_done else COLORS[ctk.get_appearance_mode()]["success"]
            
            card = make_card(self.scroll, f"Step {stage['stage_id']}: {stage['name']}", 
                             stage['simple_explanation'], stage['emoji'], color,
                             on_click=lambda s=stage: self.show_stage_detail(s))
            card.pack(fill="x", pady=5)
            
    def show_stage_detail(self, stage):
        # Create a detail view overlay or separate screen
        detail_window = ctk.CTkToplevel(self)
        detail_window.title(stage['name'])
        detail_window.geometry("700x800")
        detail_window.configure(fg_color=COLORS[ctk.get_appearance_mode()]["bg"])
        detail_window.attributes("-topmost", True)
        
        scroll = ctk.CTkScrollableFrame(detail_window, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(scroll, text=stage['emoji'], font=("Arial", 64)).pack(pady=10)
        ctk.CTkLabel(scroll, text=stage['name'], font=("Inter", 28, "bold")).pack()
        
        ctk.CTkLabel(scroll, text="Detailed Explanation", font=("Inter", 18, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["primary"]).pack(anchor="w", pady=(20, 5))
        ctk.CTkLabel(scroll, text=stage['detailed_explanation'], font=("Inter", 14), wraplength=600, justify="left").pack(anchor="w")
        
        ctk.CTkLabel(scroll, text="Why It Matters", font=("Inter", 18, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["secondary"]).pack(anchor="w", pady=(20, 5))
        ctk.CTkLabel(scroll, text=stage['why_it_matters'], font=("Inter", 14), wraplength=600, justify="left").pack(anchor="w")
        
        ctk.CTkLabel(scroll, text="Common Doubt", font=("Inter", 18, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["accent"]).pack(anchor="w", pady=(20, 5))
        q_frame = ctk.CTkFrame(scroll, fg_color=COLORS[ctk.get_appearance_mode()]["surface3"], corner_radius=10)
        q_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(q_frame, text=f"Q: {stage['common_doubt_q']}\n\nA: {stage['common_doubt_a']}", font=("Inter", 13, "italic"), wraplength=550, justify="left", padx=15, pady=15).pack()
        
        if stage['stage_id'] not in self.explored:
            btn = ctk.CTkButton(scroll, text=f"Mark as Learned (+{stage['xp_reward']} XP)", font=("Inter", 16, "bold"), height=50,
                                fg_color=COLORS[ctk.get_appearance_mode()]["success"],
                                command=lambda: self.complete_stage(stage, detail_window))
            btn.pack(pady=30)
        else:
            ctk.CTkLabel(scroll, text="✅ Already Learned", font=("Inter", 16, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["success"]).pack(pady=30)

    def complete_stage(self, stage, window):
        mark_stage_explored(stage['stage_id'], stage['name'])
        add_xp(stage['xp_reward'])
        show_xp_toast(self, stage['xp_reward'], f"Learned {stage['name']}!")
        self.explored.append(stage['stage_id'])
        window.destroy()
        # Refresh screen
        for child in self.scroll.winfo_children(): child.destroy()
        self.render_stages()
        from services.badge_engine import badge_engine
        badge_engine.check_all_badges()
