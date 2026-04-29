import customtkinter as ctk
from core.config import COLORS
from core.language import lang
from core.database import update_profile, get_profile
from core.theme import theme_manager
from ui.components import make_section_header

class SettingsScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        mode = ctk.get_appearance_mode()
        super().__init__(parent, fg_color=COLORS[mode]["bg"])
        self.nav = nav
        self.profile = get_profile()
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = make_section_header(self.scroll, lang.get("settings_title"), "Customize your JanMitra experience")
        header.pack(fill="x", pady=(0, 20))
        
        # Language Selection
        self.make_setting_group("🌐", lang.get("settings_language"))
        self.lang_var = ctk.StringVar(value=self.profile['language'])
        lang_menu = ctk.CTkOptionMenu(self.scroll, values=["en", "hi", "mr"], variable=self.lang_var, 
                                      command=self.change_language, fg_color=COLORS[mode]["primary"])
        lang_menu.pack(pady=(0, 20), anchor="w", padx=40)
        
        # Appearance Mode
        self.make_setting_group("🎨", lang.get("settings_theme"))
        self.theme_var = ctk.StringVar(value=self.profile['theme'])
        theme_menu = ctk.CTkOptionMenu(self.scroll, values=["dark", "light"], variable=self.theme_var, 
                                       command=self.change_theme, fg_color=COLORS[mode]["primary"])
        theme_menu.pack(pady=(0, 20), anchor="w", padx=40)
        
        # Font Size
        self.make_setting_group("🅰️", lang.get("settings_font"))
        self.font_var = ctk.StringVar(value=self.profile['font_size'])
        font_menu = ctk.CTkOptionMenu(self.scroll, values=["small", "medium", "large"], variable=self.font_var, 
                                      command=self.change_font, fg_color=COLORS[mode]["primary"])
        font_menu.pack(pady=(0, 20), anchor="w", padx=40)
        
        # Reset Button
        ctk.CTkButton(self.scroll, text=lang.get("settings_reset"), fg_color=COLORS[mode]["error"], 
                      height=45, width=200, command=self.reset_data).pack(pady=40, anchor="w", padx=40)

    def make_setting_group(self, emoji, title):
        ctk.CTkLabel(self.scroll, text=f"{emoji} {title}", font=("Inter", 16, "bold")).pack(anchor="w", pady=(10, 5), padx=20)

    def change_language(self, val):
        lang.set_language(val)
        update_profile(language=val)
        self.nav.switch_screen(SettingsScreen) # Refresh
        
    def change_theme(self, val):
        theme_manager.set_theme(val)
        self.nav.switch_screen(SettingsScreen) # Refresh

    def change_font(self, val):
        update_profile(font_size=val)

    def reset_data(self):
        from tkinter import messagebox
        if messagebox.askyesno("Reset Progress", "Are you sure you want to reset all your progress? This cannot be undone."):
            from core.database import reset_all_data
            reset_all_data()
            # Restart to splash
            from ui.splash import SplashScreen
            self.nav.switch_screen(SplashScreen)
