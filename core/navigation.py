class NavigationManager:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        self.sidebar = None
        self.history = []

    def switch_screen(self, screen_class, *args, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = screen_class(self.root, self, *args, **kwargs)
        self.current_frame.pack(side="right", fill="both", expand=True)
        
        # Track history for 'back' functionality if needed
        self.history.append(screen_class)

    def set_sidebar(self, sidebar_instance):
        self.sidebar = sidebar_instance

    def update_sidebar_selection(self, nav_id):
        if self.sidebar:
            self.sidebar.set_active(nav_id)
