import customtkinter as ctk
from core.config import COLORS
from core.language import lang

class SplashScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        super().__init__(parent, fg_color=COLORS[ctk.get_appearance_mode()]["bg"])
        self.nav = nav
        
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo placeholder (drawn)
        self.logo_lbl = ctk.CTkLabel(self.center_frame, text="🗳️", font=("Arial", 120))
        self.logo_lbl.pack(pady=10)
        
        self.title_lbl = ctk.CTkLabel(self.center_frame, text="JanMitra", font=("Inter", 48, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["primary"])
        self.title_lbl.pack()
        
        self.subtitle_lbl = ctk.CTkLabel(self.center_frame, text="Mera Chunav, Meri Awaaz", font=("Inter", 18), text_color=COLORS[ctk.get_appearance_mode()]["text3"])
        self.subtitle_lbl.pack(pady=(0, 40))
        
        self.prog = ctk.CTkProgressBar(self.center_frame, width=300, height=10, progress_color=COLORS[ctk.get_appearance_mode()]["primary"])
        self.prog.set(0)
        self.prog.pack()
        
        self.loading_lbl = ctk.CTkLabel(self.center_frame, text="Initializing civic awareness...", font=("Inter", 12), text_color=COLORS[ctk.get_appearance_mode()]["text3"])
        self.loading_lbl.pack(pady=10)
        
        self.progress = 0
        self.update_progress()
        
    def update_progress(self):
        self.progress += 0.05
        self.prog.set(self.progress)
        
        if self.progress >= 1:
            from core.database import get_profile
            profile = get_profile()
            if profile.get('onboarding_done'):
                from ui.home import HomeScreen
                self.nav.switch_screen(HomeScreen)
            else:
                from ui.onboarding import OnboardingScreen
                self.nav.switch_screen(OnboardingScreen)
        else:
            self.after(100, self.update_progress)
