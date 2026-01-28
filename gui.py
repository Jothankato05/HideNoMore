import customtkinter as ctk
import sys
import threading
import os
import phonenumbers
import whois
from modules import phone_lookup, username_search, metadata_extractor, domain_ip_lookup, geolocation, shodan_search, ip_by_map
import requests
import time
import random

# Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class PrintRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""

    def write(self, text):
        # Schedule the update on the main thread
        self.text_widget.after(0, self._append_text, text)

    def _append_text(self, text):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", text)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("")
        self.geometry("800x500")
        self.resizable(False, False)
        
        # Remove window decorations
        self.overrideredirect(True)
        
        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400)
        y = (self.winfo_screenheight() // 2) - (250)
        self.geometry(f"800x500+{x}+{y}")
        
        # Configure background
        self.configure(fg_color="#000000")
        
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ASCII Logo
        self.logo_text = ctk.CTkTextbox(
            self.main_frame,
            width=760,
            height=150,
            fg_color="#000000",
            text_color="#00ff00",
            font=ctk.CTkFont(family="Courier New", size=10, weight="bold")
        )
        self.logo_text.pack(pady=(10, 0))
        self.logo_text.configure(state="disabled")
        
        # System messages
        self.system_text = ctk.CTkTextbox(
            self.main_frame,
            width=760,
            height=180,
            fg_color="#000000",
            text_color="#00ff00",
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.system_text.pack(pady=10)
        self.system_text.configure(state="disabled")
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(self.main_frame, width=760, height=20)
        self.progress.pack(pady=5)
        self.progress.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00ff00"
        )
        self.status_label.pack(pady=5)
        
        # Skip instruction
        self.skip_label = ctk.CTkLabel(
            self.main_frame,
            text="Press any key to skip",
            font=ctk.CTkFont(size=10),
            text_color="#00ff0080"
        )
        self.skip_label.pack(pady=5)
        
        # State
        self.animation_running = True
        self.phase = 0
        self.skipped = False
        
        # Bind key press
        self.bind("<Key>", self.skip_intro)
        self.focus_force()
        
        # Start animation
        self.start_animation()
        
    def skip_intro(self, event=None):
        """Skip the intro animation"""
        self.skipped = True
        
    def write_text(self, widget, text, delay=30):
        """Typewriter effect"""
        widget.configure(state="normal")
        for char in text:
            if self.skipped:
                widget.insert("end", text[text.index(char):])
                break
            widget.insert("end", char)
            widget.see("end")
            widget.update()
            time.sleep(delay / 1000)
        widget.configure(state="disabled")
        
    def start_animation(self):
        """Multi-phase cinematic intro"""
        def run_intro():
            # Phase 1: ASCII Logo reveal
            ascii_logo = """
    ██╗  ██╗██╗██████╗ ███████╗    ███╗   ██╗ ██████╗ 
    ██║  ██║██║██╔══██╗██╔════╝    ████╗  ██║██╔═══██╗
    ███████║██║██║  ██║█████╗      ██╔██╗ ██║██║   ██║
    ██╔══██║██║██║  ██║██╔══╝      ██║╚██╗██║██║   ██║
    ██║  ██║██║██████╔╝███████╗    ██║ ╚████║╚██████╔╝
    ╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝    ╚═╝  ╚═══╝ ╚═════╝ 
                    ███╗   ███╗ ██████╗ ██████╗ ███████╗
                    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝
                    ██╔████╔██║██║   ██║██████╔╝█████╗  
                    ██║╚██╔╝██║██║   ██║██╔══██╗██╔══╝  
                    ██║ ╚═╝ ██║╚██████╔╝██║  ██║███████╗
                    ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
            """
            self.logo_text.configure(state="normal")
            self.logo_text.insert("1.0", ascii_logo)
            self.logo_text.configure(state="disabled")
            
            if self.skipped:
                self.finish_intro()
                return
                
            time.sleep(0.3)
            
            # Phase 2: System boot messages
            messages = [
                "[SYSTEM] Initializing OSINT Framework...",
                "[OK] Loading reconnaissance modules...",
                "[OK] Phone lookup engine ready",
                "[OK] Geolocation tracker online", 
                "[OK] Network scanner initialized",
                "[OK] Metadata extractor loaded",
                "[NETWORK] Establishing secure connections...",
                "[OK] All systems operational",
                "",
                "HIDE NO MORE - OSINT Reconnaissance Suite v1.1.0",
                "By Jothan Prime | Stealthy | Fast | Reliable"
            ]
            
            for i, msg in enumerate(messages):
                if self.skipped:
                    break
                self.write_text(self.system_text, msg + "\n", delay=15)
                self.progress.set((i + 1) / len(messages))
                if i < len(messages) - 2:
                    self.status_label.configure(text=f"Loading... {int((i + 1) / len(messages) * 100)}%")
                time.sleep(0.1 if i < 8 else 0.3)
            
            # Phase 3: Ready
            if not self.skipped:
                self.status_label.configure(text="SYSTEM READY", text_color="#00ff00")
                time.sleep(0.5)
            
            self.finish_intro()
        
        threading.Thread(target=run_intro, daemon=True).start()
    
    def finish_intro(self):
        """Complete the intro sequence"""
        self.animation_running = False
        
    def close_splash(self):
        """Close the splash screen"""
        self.animation_running = False
        self.destroy()

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("400x200")
        
        self.label = ctk.CTkLabel(self, text="Shodan API Key:")
        self.label.pack(pady=10)
        
        self.entry = ctk.CTkEntry(self, width=300)
        self.entry.pack(pady=5)
        
        # Load existing key
        self.config_path = self.get_config_path()
        if os.path.exists(self.config_path):
            try:
                import json
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.entry.insert(0, config.get('shodan_api_key', ''))
            except:
                pass

        self.save_btn = ctk.CTkButton(self, text="Save", command=self.save_config)
        self.save_btn.pack(pady=20)
        
    def get_config_path(self):
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, 'config.json')

    def save_config(self):
        import json
        key = self.entry.get().strip()
        config = {'shodan_api_key': key}
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f)
            print(f"Config saved to {self.config_path}")
            self.destroy()
        except Exception as e:
            print(f"Error saving config: {e}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hide No More - OSINT Suite")
        self.geometry("1000x700")

        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Hide No More", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_buttons = []
        tools = [
            ("Phone Lookup", self.show_phone),
            ("Username Search", self.show_username),
            ("Metadata Extraction", self.show_metadata),
            ("Domain/IP Lookup", self.show_domain),
            ("Geolocation Trace", self.show_geo),
            ("Shodan Search", self.show_shodan),
            ("Live Tracking", self.show_live),
            ("IP Map", self.show_map)
        ]

        for i, (name, command) in enumerate(tools):
            btn = ctk.CTkButton(self.sidebar_frame, text=name, command=command, fg_color="transparent", anchor="w")
            btn.grid(row=i+1, column=0, padx=20, pady=5, sticky="ew")
            self.sidebar_buttons.append(btn)


        self.appearance_mode_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=9, column=0, padx=20, pady=10, sticky="s")
        
        self.settings_btn = ctk.CTkButton(self.sidebar_frame, text="Settings", command=self.open_settings, fg_color="gray", height=24)
        self.settings_btn.grid(row=10, column=0, padx=20, pady=10, sticky="s")

        # Main Content
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(self.main_frame, text="Select a tool to begin", font=ctk.CTkFont(size=24))
        self.header_label.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Input Area (Dynamic)
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.input_label = ctk.CTkLabel(self.input_frame, text="Input:", anchor="w")
        self.input_label.grid(row=0, column=0, padx=10, pady=10)

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter target...")
        self.entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.action_button = ctk.CTkButton(self.input_frame, text="Run", command=self.run_task)
        self.action_button.grid(row=0, column=2, padx=10, pady=10)

        self.file_button = ctk.CTkButton(self.input_frame, text="Browse", command=self.browse_file, width=60)
        # Initially hidden

        # Output Console
        self.console = ctk.CTkTextbox(self.main_frame, width=800, font=("Consolas", 14), state="disabled")
        self.console.grid(row=2, column=0, sticky="nsew")

        # Redirect Stdout
        self.redirector = PrintRedirector(self.console)
        sys.stdout = self.redirector
        sys.stderr = self.redirector

        # State
        self.current_tool = None
        self.tracking_active = False

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.grab_set()


    def reset_input_ui(self):
        self.entry.delete(0, "end")
        self.file_button.grid_forget()
        self.entry.configure(state="normal")
        self.tracking_active = False

    def highlight_button(self, name):
        for btn in self.sidebar_buttons:
            if btn.cget("text") == name:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")

    def show_phone(self):
        self.header_label.configure(text="Phone Lookup")
        self.reset_input_ui()
        self.current_tool = "phone"
        self.highlight_button("Phone Lookup")

    def show_username(self):
        self.header_label.configure(text="Username Search")
        self.reset_input_ui()
        self.current_tool = "username"
        self.highlight_button("Username Search")

    def show_metadata(self):
        self.header_label.configure(text="Metadata Extraction")
        self.reset_input_ui()
        self.current_tool = "metadata"
        self.highlight_button("Metadata Extraction")
        self.file_button.grid(row=0, column=3, padx=10, pady=10)

    def show_domain(self):
        self.header_label.configure(text="Domain/IP Lookup")
        self.reset_input_ui()
        self.current_tool = "domain"
        self.highlight_button("Domain/IP Lookup")

    def show_geo(self):
        self.header_label.configure(text="Geolocation Trace")
        self.reset_input_ui()
        self.current_tool = "geo"
        self.highlight_button("Geolocation Trace")

    def show_shodan(self):
        self.header_label.configure(text="Shodan Search")
        self.reset_input_ui()
        self.current_tool = "shodan"
        self.highlight_button("Shodan Search")

    def show_live(self):
        self.header_label.configure(text="Live Tracking (Enter IP)")
        self.reset_input_ui()
        self.current_tool = "live"
        self.action_button.configure(text="Start")
        self.highlight_button("Live Tracking")

    def show_map(self):
        self.header_label.configure(text="IP Map (Generate Link)")
        self.reset_input_ui()
        self.current_tool = "map"
        self.highlight_button("IP Map")

    def browse_file(self):
        file_path = ctk.filedialog.askopenfilename()
        if file_path:
            self.entry.delete(0, "end")
            self.entry.insert(0, file_path)

    def run_task(self):
        target = self.entry.get().strip()
        if not target and self.current_tool != "live": # Live might stop with empty
            print("Please enter a target.")
            return

        if self.current_tool == "live":
            if self.tracking_active:
                self.tracking_active = False
                self.action_button.configure(text="Start")
                print("Stopping live tracking...")
            else:
                if not target:
                    print("Enter an IP to track.")
                    return
                self.tracking_active = True
                self.action_button.configure(text="Stop")
                threading.Thread(target=self.run_live_tracking, args=(target,), daemon=True).start()
            return

        # Disable button while running
        self.action_button.configure(state="disabled")
        threading.Thread(target=self.execute_tool, args=(target,), daemon=True).start()

    def execute_tool(self, target):
        print(f"\n--- Running {self.current_tool.upper()} on {target} ---\n")
        try:
            if self.current_tool == "phone":
                phone_lookup.lookup(target)
            elif self.current_tool == "username":
                username_search.search(target)
            elif self.current_tool == "metadata":
                metadata_extractor.extract(target)
            elif self.current_tool == "domain":
                domain_ip_lookup.lookup(target)
            elif self.current_tool == "geo":
                geolocation.trace(target)
            elif self.current_tool == "shodan":
                shodan_search.search(target)
            elif self.current_tool == "map":
                ip_by_map.map_ip(target)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("\n--- Task Complete ---")
            self.action_button.configure(state="normal")

    def run_live_tracking(self, target):
        print(f"Starting live tracking on {target}...")
        while self.tracking_active:
            try:
                # Custom implementation to avoid blocking wait in module
                response = requests.get(f'https://ipinfo.io/{target}/json')
                if response.status_code == 200:
                    data = response.json()
                    loc = data.get('loc')
                    if loc:
                        print(f"Location: {loc} (Time: {time.strftime('%H:%M:%S')})")
                    else:
                        print("Location not found.")
                else:
                    print(f"Error fetching data: {response.status_code}")
            except Exception as e:
                print(f"Tracking error: {e}")
            
            for _ in range(10): # Check stop every second for 10 seconds
                if not self.tracking_active: break
                time.sleep(1)

if __name__ == "__main__":
    # Create main app but keep it hidden
    app = App()
    app.withdraw()
    
    # Create and show splash screen
    splash = SplashScreen(app)
    
    def finish_loading():
        time.sleep(5)  # Give time for full cinematic intro (can be skipped)
        splash.close_splash()
        app.deiconify()  # Show the main app
    
    # Schedule the transition
    app.after(100, lambda: threading.Thread(target=finish_loading, daemon=True).start())
    app.mainloop()
