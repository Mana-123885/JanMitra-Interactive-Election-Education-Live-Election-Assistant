import customtkinter as ctk
import time
from core.config import COLORS
from core.language import lang
from services.quiz_engine import quiz_engine
from ui.components import make_section_header, make_quiz_option_button, show_xp_toast

class QuizScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        mode = ctk.get_appearance_mode()
        super().__init__(parent, fg_color=COLORS[mode]["bg"])
        self.nav = nav
        
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=40, pady=40)
        
        self.show_category_selection()
        
    def show_category_selection(self):
        for widget in self.content.winfo_children(): widget.destroy()
        
        header = make_section_header(self.content, lang.get("quiz_title"), "Select a category to test your knowledge")
        header.pack(pady=(0, 30))
        
        categories = ["Basics", "Types", "VotingDay", "Leaders", "Myths", "All"]
        for cat in categories:
            btn = ctk.CTkButton(self.content, text=cat, font=("Inter", 18, "bold"), height=60, width=400,
                                fg_color=COLORS[ctk.get_appearance_mode()]["surface2"],
                                hover_color=COLORS[ctk.get_appearance_mode()]["primary"],
                                command=lambda c=cat: self.start_quiz(c))
            btn.pack(pady=10)
            
    def start_quiz(self, category):
        self.category = category
        self.questions = quiz_engine.get_quiz_session(category)
        self.current_idx = 0
        self.score = 0
        self.start_time = time.time()
        self.show_question()
        
    def show_question(self):
        for widget in self.content.winfo_children(): widget.destroy()
        
        q = self.questions[self.current_idx]
        
        # Progress
        prog_lbl = ctk.CTkLabel(self.content, text=f"Question {self.current_idx+1} of {len(self.questions)}", font=("Inter", 14))
        prog_lbl.pack(pady=(0, 10))
        
        prog_bar = ctk.CTkProgressBar(self.content, width=400)
        prog_bar.set((self.current_idx + 1) / len(self.questions))
        prog_bar.pack(pady=(0, 30))
        
        # Question
        q_lbl = ctk.CTkLabel(self.content, text=q['q'], font=("Inter", 22, "bold"), wraplength=600)
        q_lbl.pack(pady=20)
        
        # Options
        self.opt_buttons = []
        for i, opt in enumerate(q['opts']):
            btn = make_quiz_option_button(self.content, opt, on_click=lambda idx=i: self.check_answer(idx))
            btn.pack(fill="x", pady=5)
            self.opt_buttons.append(btn)
            
    def check_answer(self, idx):
        q = self.questions[self.current_idx]
        correct = q['correct']
        
        for i, btn in enumerate(self.opt_buttons):
            btn.configure(state="disabled")
            if i == correct:
                btn.configure(fg_color=COLORS[ctk.get_appearance_mode()]["success"])
            elif i == idx:
                btn.configure(fg_color=COLORS[ctk.get_appearance_mode()]["error"])
        
        if idx == correct:
            self.score += 1
            show_xp_toast(self, 10, "Correct!")
        
        # Show explanation
        exp_lbl = ctk.CTkLabel(self.content, text=q['exp'], font=("Inter", 14, "italic"), wraplength=600, text_color=COLORS[ctk.get_appearance_mode()]["text2"])
        exp_lbl.pack(pady=20)
        
        next_btn = ctk.CTkButton(self.content, text="Next Question" if self.current_idx < len(self.questions)-1 else "Show Results",
                                 font=("Inter", 16, "bold"), height=50, command=self.next_step)
        next_btn.pack(pady=20)
        
    def next_step(self):
        if self.current_idx < len(self.questions) - 1:
            self.current_idx += 1
            self.show_question()
        else:
            self.show_results()
            
    def show_results(self):
        for widget in self.content.winfo_children(): widget.destroy()
        
        time_taken = int(time.time() - self.start_time)
        xp, badge = quiz_engine.process_result(self.category, self.score, len(self.questions), time_taken)
        
        ctk.CTkLabel(self.content, text="🎯", font=("Arial", 80)).pack(pady=20)
        ctk.CTkLabel(self.content, text=lang.get("quiz_result"), font=("Inter", 32, "bold")).pack()
        
        score_text = lang.get("quiz_score", s=self.score, t=len(self.questions))
        ctk.CTkLabel(self.content, text=score_text, font=("Inter", 24)).pack(pady=10)
        
        xp_text = lang.get("quiz_xp_earned", xp=xp)
        ctk.CTkLabel(self.content, text=xp_text, font=("Inter", 18, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["primary"]).pack()
        
        if self.score == len(self.questions):
            ctk.CTkLabel(self.content, text=lang.get("quiz_perfect"), font=("Inter", 20, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["gold"]).pack(pady=10)
            
        btn_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        btn_frame.pack(pady=40)
        
        ctk.CTkButton(btn_frame, text=lang.get("quiz_retry"), font=("Inter", 16), height=50, width=200, command=self.show_category_selection).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Finish", font=("Inter", 16, "bold"), height=50, width=200, fg_color=COLORS[ctk.get_appearance_mode()]["primary"], 
                      command=lambda: self.nav.switch_screen(HomeScreen)).pack(side="left", padx=10)

from ui.home import HomeScreen
import random
