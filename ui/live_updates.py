import customtkinter as ctk
from core.config import COLORS
from core.language import lang
from services.live_data import live_data_service
from ui.components import make_section_header

class LiveUpdatesScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        mode = ctk.get_appearance_mode()
        super().__init__(parent, fg_color=COLORS[mode]["bg"])
        self.nav = nav
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=20)
        
        header = make_section_header(self.header_frame, lang.get("live_title"), lang.get("live_last_updated", t=live_data_service.get_last_updated_string()))
        header.pack(side="left")
        
        refresh_btn = ctk.CTkButton(self.header_frame, text=lang.get("live_refresh"), width=100, command=self.refresh)
        refresh_btn.pack(side="right")
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.render_updates()
        
    def render_updates(self):
        for widget in self.scroll.winfo_children(): widget.destroy()
        
        updates = live_data_service.get_updates()
        for up in updates:
            card = ctk.CTkFrame(self.scroll, fg_color=COLORS[ctk.get_appearance_mode()]["surface2"], corner_radius=15, border_width=1, border_color=COLORS[ctk.get_appearance_mode()]["border"])
            card.pack(fill="x", pady=10)
            
            title_row = ctk.CTkFrame(card, fg_color="transparent")
            title_row.pack(fill="x", padx=20, pady=(15, 5))
            
            ctk.CTkLabel(title_row, text=f"{up['state']} {up['election_type']}", font=("Inter", 18, "bold")).pack(side="left")
            
            status_col = COLORS[ctk.get_appearance_mode()]["success"] if up['status'] == "Completed" else COLORS[ctk.get_appearance_mode()]["warning"]
            status_lbl = ctk.CTkFrame(title_row, fg_color=status_col, corner_radius=5)
            status_lbl.pack(side="right")
            ctk.CTkLabel(status_lbl, text=up['status'], font=("Inter", 11, "bold"), text_color="white", padx=10).pack()
            
            ctk.CTkLabel(card, text=up['description'], font=("Inter", 14), wraplength=600, justify="left").pack(anchor="w", padx=20, pady=5)
            
            date_lbl = ctk.CTkLabel(card, text=f"📅 {up['date']} | {up['phases_total']} Phases", font=("Inter", 12), text_color=COLORS[ctk.get_appearance_mode()]["text3"])
            date_lbl.pack(anchor="w", padx=20, pady=(0, 15))

    def refresh(self):
        self.render_updates()
