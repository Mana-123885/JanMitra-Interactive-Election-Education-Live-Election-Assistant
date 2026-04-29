import customtkinter as ctk
from core.config import COLORS
from core.language import lang
from core.database import update_profile

class OnboardingScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        super().__init__(parent, fg_color=COLORS[ctk.get_appearance_mode()]["bg"])
        self.nav = nav
        self.step = 1
        
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.place(relx=0.5, rely=0.5, anchor="center")
        
        self.show_step_1()
        
    def show_step_1(self):
        for widget in self.content.winfo_children(): widget.destroy()
        
        ctk.CTkLabel(self.content, text="🌐", font=("Arial", 64)).pack(pady=20)
        ctk.CTkLabel(self.content, text=lang.get("onboarding_lang"), font=("Inter", 24, "bold")).pack(pady=10)
        
        langs = [("English", "en"), ("हिंदी", "hi"), ("मराठी", "mr")]
        for name, code in langs:
            btn = ctk.CTkButton(self.content, text=name, font=("Inter", 16), height=45, width=200,
                                fg_color=COLORS[ctk.get_appearance_mode()]["surface3"],
                                text_color=COLORS[ctk.get_appearance_mode()]["text1"],
                                hover_color=COLORS[ctk.get_appearance_mode()]["primary"],
                                command=lambda c=code: self.set_lang(c))
            btn.pack(pady=5)

    def set_lang(self, code):
        lang.set_language(code)
        update_profile(language=code)
        self.show_step_2()
        
    def show_step_2(self):
        for widget in self.content.winfo_children(): widget.destroy()
        
        ctk.CTkLabel(self.content, text="👋", font=("Arial", 64)).pack(pady=20)
        ctk.CTkLabel(self.content, text=lang.get("onboarding_who"), font=("Inter", 24, "bold")).pack(pady=10)
        
        self.name_entry = ctk.CTkEntry(self.content, placeholder_text="Your Name", width=300, height=45, font=("Inter", 14))
        self.name_entry.pack(pady=20)
        
        btn = ctk.CTkButton(self.content, text="Next", font=("Inter", 16, "bold"), height=45, width=300,
                            fg_color=COLORS[ctk.get_appearance_mode()]["primary"],
                            command=self.finish_onboarding)
        btn.pack(pady=10)
        
    def finish_onboarding(self):
        name = self.name_entry.get() or "Voter"
        update_profile(name=name, onboarding_done=1)
        from ui.home import HomeScreen
        self.nav.switch_screen(HomeScreen)
