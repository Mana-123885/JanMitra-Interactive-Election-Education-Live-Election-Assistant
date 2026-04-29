import customtkinter as ctk
from core.config import COLORS
from core.language import lang
from core.database import add_xp, earn_badge
from ui.components import make_section_header, show_xp_toast

class PollingSimulatorScreen(ctk.CTkFrame):
    def __init__(self, parent, nav):
        mode = ctk.get_appearance_mode()
        super().__init__(parent, fg_color=COLORS[mode]["bg"])
        self.nav = nav
        self.step_idx = 0
        
        self.steps = [
            {
                "title": "Before You Go",
                "emoji": "🏠",
                "desc": "Check your name on Electoral Roll (electoralsearch.eci.gov.in), find your booth, and keep your Voter ID or 12 alternative documents ready.",
                "action": "Do you have your ID ready?",
                "choices": ["Yes, I'm ready!", "No, I'll go without ID"],
                "correct": 0,
                "wrong_msg": "Wait! You cannot vote without a valid ID that matches the Voter List."
            },
            {
                "title": "At the Polling Station",
                "emoji": "🏢",
                "desc": "Identify your booth from the list outside, join the correct queue for your serial number range.",
                "action": "Where do you go?",
                "choices": ["Any booth", "My assigned booth"],
                "correct": 1,
                "wrong_msg": "Each voter is assigned a specific booth. You cannot vote in any other booth."
            },
            {
                "title": "Queue & Verification",
                "emoji": "👨‍👩‍👧‍👦",
                "desc": "First polling officer checks your name in the roll and verifies your photo ID.",
                "action": "Present your document...",
                "choices": ["Show ID", "Argue about the list"],
                "correct": 0,
                "wrong_msg": "Cooperation is key. The officer must verify you against the official roll."
            },
            {
                "title": "Indelible Ink",
                "emoji": "☝️",
                "desc": "Second polling officer applies indelible ink to your left index finger and records your serial number.",
                "action": "Extend your finger...",
                "choices": ["Accept the ink", "Refuse the ink"],
                "correct": 0,
                "wrong_msg": "The ink is mandatory to prevent multiple voting. Refusal means you can't vote."
            },
            {
                "title": "At the EVM",
                "emoji": "🗳️",
                "desc": "Go to the voting compartment. Find your candidate on the EVM (name + symbol + serial number).",
                "action": "Cast your vote...",
                "choices": ["Press the blue button", "Take a photo of EVM"],
                "correct": 0,
                "wrong_msg": "Photography inside the booth is strictly prohibited to maintain secrecy of the ballot."
            },
            {
                "title": "VVPAT Verification",
                "emoji": "📄",
                "desc": "Watch the VVPAT slip for 7 seconds — confirm it shows your chosen candidate's details. The slip then drops into a sealed box.",
                "action": "Verify the slip...",
                "choices": ["Wait 7 seconds", "Leave immediately"],
                "correct": 0,
                "wrong_msg": "It's best to wait and verify that your vote was recorded correctly."
            },
            {
                "title": "Exit",
                "emoji": "🚪",
                "desc": "Exit the polling station quietly. Remember, your vote is secret.",
                "action": "Leaving the booth...",
                "choices": ["Tell everyone who I voted for", "Keep it secret"],
                "correct": 1,
                "wrong_msg": "Maintaining a secret ballot is your right and duty. You shouldn't disclose it in the booth area."
            },
            {
                "title": "Completion",
                "emoji": "🏅",
                "desc": "Congratulations! You have successfully cast your vote and fulfilled your civic duty.",
                "action": "Final Step",
                "choices": ["Get my badge!", "Do it again"],
                "correct": 0,
                "wrong_msg": "You can only vote once per election!"
            }
        ]
        
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.place(relx=0.5, rely=0.5, anchor="center")
        
        self.show_step()
        
    def show_step(self):
        for widget in self.content.winfo_children(): widget.destroy()
        
        step = self.steps[self.step_idx]
        
        ctk.CTkLabel(self.content, text=f"Step {self.step_idx + 1} of 8", font=("Inter", 14)).pack()
        prog = ctk.CTkProgressBar(self.content, width=400)
        prog.set((self.step_idx + 1) / 8)
        prog.pack(pady=10)
        
        ctk.CTkLabel(self.content, text=step['emoji'], font=("Arial", 80)).pack(pady=20)
        ctk.CTkLabel(self.content, text=step['title'], font=("Inter", 28, "bold")).pack()
        ctk.CTkLabel(self.content, text=step['desc'], font=("Inter", 16), wraplength=500, pady=20).pack()
        
        ctk.CTkLabel(self.content, text=step['action'], font=("Inter", 14, "bold"), text_color=COLORS[ctk.get_appearance_mode()]["primary"]).pack()
        
        btn_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        for i, choice in enumerate(step['choices']):
            btn = ctk.CTkButton(btn_frame, text=choice, height=45, width=200, 
                                command=lambda idx=i: self.check_choice(idx))
            btn.pack(side="left", padx=10)
            
    def check_choice(self, idx):
        step = self.steps[self.step_idx]
        if idx == step['correct']:
            add_xp(15)
            show_xp_toast(self, 15, "Correct action!")
            if self.step_idx < 7:
                self.step_idx += 1
                self.show_step()
            else:
                self.finish_simulator()
        else:
            self.show_error(step['wrong_msg'])
            
    def show_error(self, msg):
        err_window = ctk.CTkToplevel(self)
        err_window.title("Mistake!")
        err_window.geometry("400x300")
        err_window.attributes("-topmost", True)
        
        ctk.CTkLabel(err_window, text="❌", font=("Arial", 64)).pack(pady=20)
        ctk.CTkLabel(err_window, text=msg, font=("Inter", 14), wraplength=350).pack(pady=20)
        ctk.CTkButton(err_window, text="Try Again", command=err_window.destroy).pack(pady=10)
        
    def finish_simulator(self):
        earn_badge("voter_ready")
        from ui.home import HomeScreen
        self.nav.switch_screen(HomeScreen)
        show_xp_toast(self.nav.root, 100, "Voter Ready Badge Earned!")
