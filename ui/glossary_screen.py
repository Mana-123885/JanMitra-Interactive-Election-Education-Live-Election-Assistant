import customtkinter as ctk
import json
from core.config import COLORS
from core.language import lang
from core.database import mark_glossary_read, add_bookmark, get_bookmarks, remove_bookmark
from ui.components import make_section_header

class GlossaryScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        mode = ctk.get_appearance_mode()
        super().__init__(parent, fg_color=COLORS[mode]["bg"])
        self.nav = nav
        
        with open("data/glossary.json", "r", encoding="utf-8") as f:
            self.terms = json.load(f)
            
        self.bookmarks = [b['item_id'] for b in get_bookmarks() if b['item_type'] == 'glossary']
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=20)
        
        header = make_section_header(self.header_frame, lang.get("glossary_title"), "Learn the language of democracy")
        header.pack(side="left")
        
        # Search
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_terms)
        self.search_entry = ctk.CTkEntry(self.header_frame, placeholder_text=lang.get("glossary_search"), width=250, textvariable=self.search_var)
        self.search_entry.pack(side="right", pady=10)
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.render_terms(self.terms)
        
    def render_terms(self, term_list):
        for widget in self.scroll.winfo_children(): widget.destroy()
        
        current_letter = ""
        for term in sorted(term_list, key=lambda x: x['term']):
            if term['term'][0].upper() != current_letter:
                current_letter = term['term'][0].upper()
                ctk.CTkLabel(self.scroll, text=current_letter, font=("Inter", 20, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["primary"]).pack(anchor="w", pady=(15, 5), padx=10)
            
            self.make_term_card(term)
            
    def make_term_card(self, term):
        card = ctk.CTkFrame(self.scroll, fg_color=COLORS[ctk.get_appearance_mode()]["surface2"], corner_radius=12)
        card.pack(fill="x", pady=5)
        
        title_row = ctk.CTkFrame(card, fg_color="transparent")
        title_row.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(title_row, text=term['term'], font=("Inter", 16, "bold")).pack(side="left")
        
        is_bookmarked = term['term'] in self.bookmarks
        btn_text = "⭐" if is_bookmarked else "☆"
        bookmark_btn = ctk.CTkButton(title_row, text=btn_text, width=30, height=30, fg_color="transparent", 
                                     text_color=COLORS[ctk.get_appearance_mode()]["gold"], font=("Arial", 18),
                                     command=lambda t=term: self.toggle_bookmark(t))
        bookmark_btn.pack(side="right")
        
        ctk.CTkLabel(card, text=term['definition'], font=("Inter", 14), wraplength=650, justify="left").pack(anchor="w", padx=15, pady=(0, 5))
        ctk.CTkLabel(card, text=f"Example: {term['example']}", font=("Inter", 12, "italic"), text_color=COLORS[ctk.get_appearance_mode()]["text3"]).pack(anchor="w", padx=15, pady=(0, 10))
        
        mark_glossary_read(term['term']) # Mark as read when rendered

    def filter_terms(self, *args):
        query = self.search_var.get().lower()
        filtered = [t for t in self.terms if query in t['term'].lower() or query in t['definition'].lower()]
        self.render_terms(filtered)

    def toggle_bookmark(self, term):
        if term['term'] in self.bookmarks:
            remove_bookmark(term['term'])
            self.bookmarks.remove(term['term'])
        else:
            add_bookmark('glossary', term['term'], term['term'], term['definition'])
            self.bookmarks.append(term['term'])
        self.filter_terms()
        from services.badge_engine import badge_engine
        badge_engine.check_all_badges()
