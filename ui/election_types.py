import customtkinter as ctk
from core.config import COLORS
from core.language import lang
from ui.components import make_section_header, make_card

class ElectionTypesScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        mode = ctk.get_appearance_mode()
        super().__init__(parent, fg_color=COLORS[mode]["bg"])
        self.nav = nav
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = make_section_header(self.scroll, lang.get("nav_types"), "Understand different levels of Indian democracy")
        header.pack(fill="x", pady=(0, 20))
        
        types = [
            ("Lok Sabha", "General Elections for the lower house of Parliament. Directly elected by people.", "🏛️", COLORS[mode]["primary"]),
            ("Rajya Sabha", "Upper house of Parliament. Indirectly elected by MLAs.", "📜", COLORS[mode]["secondary"]),
            ("Vidhan Sabha", "State Assembly elections to choose MLAs and state government.", "🏰", COLORS[mode]["accent"]),
            ("By-Elections", "Held to fill a single vacant seat due to death or resignation.", "🔄", COLORS[mode]["success"]),
            ("Local Bodies", "Panchayats and Municipal elections for local governance.", "🏡", COLORS[mode]["warning"])
        ]
        
        for name, desc, emoji, col in types:
            card = make_card(self.scroll, name, desc, emoji, col, on_click=lambda n=name: self.show_detail(n))
            card.pack(fill="x", pady=5)
            
    def show_detail(self, name):
        # Placeholder for detailed type info
        pass
