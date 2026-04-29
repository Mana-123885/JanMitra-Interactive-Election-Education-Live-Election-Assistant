import customtkinter as ctk
from core.config import COLORS
from core.language import lang
from core.database import get_chat_history, clear_chat_history
from ui.components import make_section_header, make_chat_bubble, make_typing_indicator
from services.chatbot import chatbot_service

class ChatbotScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        mode = ctk.get_appearance_mode()
        super().__init__(parent, fg_color=COLORS[mode]["bg"])
        self.nav = nav
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        header = make_section_header(header_frame, lang.get("chatbot_title"), lang.get("chatbot_disclaimer"))
        header.pack(side="left")
        
        clear_btn = ctk.CTkButton(header_frame, text=lang.get("chatbot_clear"), fg_color=COLORS[mode]["error"], 
                                  width=100, command=self.clear_chat)
        clear_btn.pack(side="right")
        
        # Chat area
        self.chat_scroll = ctk.CTkScrollableFrame(self, fg_color=COLORS[mode]["surface"], corner_radius=15)
        self.chat_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Input area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text=lang.get("chatbot_placeholder"), height=50, font=("Inter", 14))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.send_message())
        
        self.send_btn = ctk.CTkButton(self.input_frame, text=lang.get("chatbot_send"), width=100, height=50, 
                                      fg_color=COLORS[mode]["primary"], font=("Inter", 14, "bold"),
                                      command=self.send_message)
        self.send_btn.pack(side="right")
        
        self.load_history()
        
    def load_history(self):
        history = get_chat_history()
        for msg in history:
            make_chat_bubble(self.chat_scroll, msg['message'], msg['role'])
        self.scroll_to_bottom()
            
    def send_message(self):
        query = self.entry.get()
        if not query.strip(): return
        
        self.entry.delete(0, 'end')
        make_chat_bubble(self.chat_scroll, query, "user")
        self.scroll_to_bottom()
        
        # Bot thinking...
        self.after(500, self.bot_reply, query)
        
    def bot_reply(self, query):
        response = chatbot_service.get_response(query)
        make_chat_bubble(self.chat_scroll, response, "bot")
        self.scroll_to_bottom()
        from services.badge_engine import badge_engine
        badge_engine.check_all_badges()
        
    def clear_chat(self):
        clear_chat_history()
        for widget in self.chat_scroll.winfo_children(): widget.destroy()
        
    def scroll_to_bottom(self):
        self.update_idletasks()
        self.chat_scroll._parent_canvas.yview_moveto(1.0)
