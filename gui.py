import customtkinter as ctk
import sys
import threading
import os
from modules import phone_lookup, username_search, metadata_extractor, domain_ip_lookup, geolocation, shodan_search, ip_by_map
import requests
import time

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
        self.appearance_mode_menu.grid(row=9, column=0, padx=20, pady=20, sticky="s")

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
    app = App()
    app.mainloop()
