import customtkinter as ctk
from PIL import Image, ImageDraw
import time
from core.config import COLORS
from core.language import lang

def make_card(parent, title, subtitle, emoji, color, on_click=None, badge=None):
    """Returns a styled CTkFrame card with hover effect."""
    card = ctk.CTkFrame(parent, fg_color=COLORS[ctk.get_appearance_mode()]["surface2"], corner_radius=15, border_width=1, border_color=COLORS[ctk.get_appearance_mode()]["border"])
    
    # Left emoji indicator
    emoji_label = ctk.CTkLabel(card, text=emoji, font=("Arial", 32), width=60)
    emoji_label.pack(side="left", padx=15, pady=15)
    
    # Text container
    text_frame = ctk.CTkFrame(card, fg_color="transparent")
    text_frame.pack(side="left", fill="both", expand=True, pady=15)
    
    title_label = ctk.CTkLabel(text_frame, text=title, font=("Inter", 18, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["text1"], anchor="w")
    title_label.pack(fill="x")
    
    subtitle_label = ctk.CTkLabel(text_frame, text=subtitle, font=("Inter", 13), text_color=COLORS[ctk.get_appearance_mode()]["text3"], anchor="w", wraplength=400)
    subtitle_label.pack(fill="x")
    
    if on_click:
        card.bind("<Button-1>", lambda e: on_click())
        for child in [emoji_label, text_frame, title_label, subtitle_label]:
            child.bind("<Button-1>", lambda e: on_click())
            
        def on_enter(e):
            card.configure(fg_color=COLORS[ctk.get_appearance_mode()]["card_hover"], border_color=COLORS[ctk.get_appearance_mode()]["primary"])
        def on_leave(e):
            card.configure(fg_color=COLORS[ctk.get_appearance_mode()]["surface2"], border_color=COLORS[ctk.get_appearance_mode()]["border"])
            
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
    return card

def make_progress_card(parent, title, current, total, color):
    card = ctk.CTkFrame(parent, fg_color=COLORS[ctk.get_appearance_mode()]["surface2"], corner_radius=12)
    card.pack(fill="x", padx=10, pady=5)
    
    lbl = ctk.CTkLabel(card, text=f"{title}: {current}/{total}", font=("Inter", 14, "bold"))
    lbl.pack(padx=15, pady=(10, 0), anchor="w")
    
    prog = ctk.CTkProgressBar(card, progress_color=color)
    prog.set(current/total if total > 0 else 0)
    prog.pack(fill="x", padx=15, pady=(5, 15))
    return card

def make_stat_chip(parent, emoji, value, label, color):
    chip = ctk.CTkFrame(parent, fg_color=COLORS[ctk.get_appearance_mode()]["surface3"], corner_radius=10, height=80)
    
    val_lbl = ctk.CTkLabel(chip, text=f"{emoji} {value}", font=("Inter", 20, "bold"), text_color=color)
    val_lbl.pack(pady=(10, 0))
    
    lab_lbl = ctk.CTkLabel(chip, text=label, font=("Inter", 11), text_color=COLORS[ctk.get_appearance_mode()]["text3"])
    lab_lbl.pack(pady=(0, 10))
    
    return chip

def make_section_header(parent, title, subtitle=None):
    header = ctk.CTkFrame(parent, fg_color="transparent")
    
    t_lbl = ctk.CTkLabel(header, text=title, font=("Inter", 24, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["text1"])
    t_lbl.pack(anchor="w")
    
    if subtitle:
        s_lbl = ctk.CTkLabel(header, text=subtitle, font=("Inter", 14), text_color=COLORS[ctk.get_appearance_mode()]["text3"])
        s_lbl.pack(anchor="w")
        
    return header

def make_nav_button(parent, emoji, label, is_active, on_click):
    mode = ctk.get_appearance_mode()
    bg = COLORS[mode]["primary"] if is_active else "transparent"
    fg = COLORS[mode]["text1"] if is_active else COLORS[mode]["text2"]
    
    btn = ctk.CTkButton(parent, text=f"{emoji}  {label}", font=("Inter", 14, "bold" if is_active else "normal"),
                        fg_color=bg, text_color=fg, anchor="w", corner_radius=10, height=45,
                        hover_color=COLORS[mode]["surface3"], command=on_click)
    return btn

def make_level_badge(parent, level_dict, xp, next_level_xp):
    container = ctk.CTkFrame(parent, fg_color=COLORS[ctk.get_appearance_mode()]["surface2"], corner_radius=15, border_width=1, border_color=COLORS[ctk.get_appearance_mode()]["border"])
    
    emoji_lbl = ctk.CTkLabel(container, text=level_dict["emoji"], font=("Arial", 40))
    emoji_lbl.pack(pady=(15, 0))
    
    name_lbl = ctk.CTkLabel(container, text=level_dict["title"], font=("Inter", 18, "bold"), text_color=level_dict["color"])
    name_lbl.pack()
    
    xp_lbl = ctk.CTkLabel(container, text=f"{xp} XP", font=("Inter", 12), text_color=COLORS[ctk.get_appearance_mode()]["text3"])
    xp_lbl.pack()
    
    prog = ctk.CTkProgressBar(container, progress_color=level_dict["color"], height=8)
    prog.set(xp/next_level_xp if next_level_xp > 0 else 1)
    prog.pack(fill="x", padx=20, pady=(10, 20))
    
    return container

def make_badge_tile(parent, badge_dict, earned):
    mode = ctk.get_appearance_mode()
    container = ctk.CTkFrame(parent, fg_color=COLORS[mode]["surface2"] if earned else COLORS[mode]["bg"], 
                            corner_radius=12, border_width=2, 
                            border_color=COLORS[mode]["gold"] if earned else COLORS[mode]["border"])
    
    emoji_lbl = ctk.CTkLabel(container, text=badge_dict["emoji"], font=("Arial", 36))
    if not earned: emoji_lbl.configure(text_color="gray")
    emoji_lbl.pack(pady=(10, 0))
    
    name_lbl = ctk.CTkLabel(container, text=badge_dict["name"], font=("Inter", 11, "bold"), 
                            text_color=COLORS[mode]["text1"] if earned else COLORS[mode]["text3"])
    name_lbl.pack(pady=(0, 10))
    
    return container

def make_quiz_option_button(parent, text, on_click, state="normal"):
    btn = ctk.CTkButton(parent, text=text, font=("Inter", 14), height=50, corner_radius=10,
                        fg_color=COLORS[ctk.get_appearance_mode()]["surface3"],
                        text_color=COLORS[ctk.get_appearance_mode()]["text1"],
                        hover_color=COLORS[ctk.get_appearance_mode()]["primary"],
                        command=on_click, state=state)
    return btn

def make_chat_bubble(parent, message, role, timestamp=None):
    mode = ctk.get_appearance_mode()
    is_user = role == "user"
    
    bubble_frame = ctk.CTkFrame(parent, fg_color="transparent")
    bubble_frame.pack(fill="x", pady=5)
    
    align = "right" if is_user else "left"
    bg = COLORS[mode]["primary"] if is_user else COLORS[mode]["surface3"]
    text_col = COLORS[mode]["text1"]
    
    bubble = ctk.CTkFrame(bubble_frame, fg_color=bg, corner_radius=15)
    bubble.pack(side=align, padx=10)
    
    msg_lbl = ctk.CTkLabel(bubble, text=message, font=("Inter", 13), wraplength=350, justify="left", text_color=text_col)
    msg_lbl.pack(padx=15, pady=10)
    
    return bubble_frame

def show_xp_toast(parent, amount, message="XP Earned!"):
    toast = ctk.CTkFrame(parent, fg_color=COLORS[ctk.get_appearance_mode()]["success"], corner_radius=20)
    toast.place(relx=0.5, rely=0.1, anchor="center")
    
    lbl = ctk.CTkLabel(toast, text=f"✨ {message} +{amount} XP", font=("Inter", 14, "bold"), text_color="white")
    lbl.pack(padx=20, pady=10)
    
    def fade():
        toast.destroy()
    parent.after(2000, fade)

def show_levelup_popup(parent, new_level, on_close):
    popup = ctk.CTkToplevel(parent)
    popup.title("Level Up!")
    popup.geometry("500x600")
    popup.attributes("-topmost", True)
    popup.configure(fg_color=COLORS[ctk.get_appearance_mode()]["bg"])
    
    # Center popup
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() // 2) - (500 // 2)
    y = (popup.winfo_screenheight() // 2) - (600 // 2)
    popup.geometry(f"+{x}+{y}")
    
    ctk.CTkLabel(popup, text="🎉", font=("Arial", 80)).pack(pady=(40, 10))
    ctk.CTkLabel(popup, text=lang.get("level_up_title"), font=("Inter", 32, "bold")).pack()
    
    level_card = make_level_badge(popup, new_level, new_level["xp"], new_level["xp"])
    level_card.pack(pady=30, padx=50)
    
    ctk.CTkLabel(popup, text=new_level["desc"], font=("Inter", 16), wraplength=400).pack(pady=10)
    
    btn = ctk.CTkButton(popup, text="Awesome! 🙌", font=("Inter", 16, "bold"), height=50, 
                        fg_color=COLORS[ctk.get_appearance_mode()]["primary"], command=lambda: [popup.destroy(), on_close()])
    btn.pack(pady=30)
    
    # Animated confetti (simple version)
    for _ in range(30):
        color = random.choice([COLORS[ctk.get_appearance_mode()]["primary"], COLORS[ctk.get_appearance_mode()]["secondary"], COLORS[ctk.get_appearance_mode()]["gold"]])
        dot = ctk.CTkLabel(popup, text="•", text_color=color, font=("Arial", 24))
        dot.place(x=random.randint(0, 500), y=random.randint(0, 600))

def make_typing_indicator(parent):
    """Returns an animated typing indicator (. .. ...) using .after()."""
    indicator = ctk.CTkLabel(parent, text=".  ", font=("Inter", 24, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["primary"])
    
    def animate(step=0):
        dots = [".  ", ".. ", "...", "   "]
        if indicator.winfo_exists():
            indicator.configure(text=dots[step % 4])
            indicator.after(400, lambda: animate(step + 1))
            
    animate()
    return indicator

import random
