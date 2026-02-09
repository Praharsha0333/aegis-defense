import tkinter as tk
from tkinter import ttk, font
import threading
import time
from playwright.sync_api import sync_playwright
from src.bodyguard import BrowserBodyguard

class AegisDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Aegis Defense System | Command & Control")
        self.root.geometry("1200x800")
        
        # --- THEME COLORS (High Contrast Cyber) ---
        self.colors = {
            "bg_dark": "#050505",       # Pure Black
            "bg_panel": "#111111",      # Dark Grey
            "text_main": "#e0e0e0",     # Bright Grey
            "neon_green": "#00ff41",    # Matrix Green
            "neon_red": "#ff3333",      # Alert Red
            "neon_cyan": "#00ffff",     # Cyber Cyan
            "neon_yellow": "#ffff00",   # Warning Yellow
        }
        
        self.root.configure(bg=self.colors["bg_dark"])

        # --- FONTS ---
        self.font_header = ("Impact", 26)
        self.font_table = ("Consolas", 11)
        self.font_btn = ("Segoe UI", 12, "bold")

        # --- STYLE CONFIGURATION ---
        style = ttk.Style()
        style.theme_use("clam")
        
        # Table Styling
        style.configure("Treeview", 
                        background="#0a0a0a",
                        foreground="white",
                        fieldbackground="#0a0a0a",
                        rowheight=35,
                        font=self.font_table,
                        borderwidth=0)
        
        style.configure("Treeview.Heading", 
                        background="#222",
                        foreground=self.colors["neon_cyan"],
                        font=("Segoe UI", 11, "bold"))
        
        style.map("Treeview", background=[("selected", "#222")])

        # =================================================================
        # 1. HEADER
        # =================================================================
        self.header_frame = tk.Frame(root, bg=self.colors["bg_panel"], pady=20, padx=25)
        self.header_frame.pack(fill="x", pady=(0, 2))

        # Logo / Title
        title_box = tk.Frame(self.header_frame, bg=self.colors["bg_panel"])
        title_box.pack(side="left")
        
        tk.Label(title_box, text="🛡️", font=("Segoe UI", 30), bg=self.colors["bg_panel"]).pack(side="left")
        tk.Label(title_box, text="AEGIS", font=self.font_header, fg="white", bg=self.colors["bg_panel"]).pack(side="left", padx=(10, 0))
        tk.Label(title_box, text="SECURITY", font=self.font_header, fg=self.colors["neon_green"], bg=self.colors["bg_panel"]).pack(side="left")

        # Risk Scoreboard
        self.score_frame = tk.Frame(self.header_frame, bg=self.colors["bg_panel"])
        self.score_frame.pack(side="right")
        
        self.risk_label_title = tk.Label(self.score_frame, text="CURRENT RISK LEVEL", 
                                        font=("Consolas", 10, "bold"), bg=self.colors["bg_panel"], fg="#666")
        self.risk_label_title.pack(anchor="e")
        
        self.risk_val_label = tk.Label(self.score_frame, text="0/100 (SECURE)", 
                                       font=("Impact", 28), bg=self.colors["bg_panel"], fg=self.colors["neon_green"])
        self.risk_val_label.pack(anchor="e")

        # =================================================================
        # 2. COMMAND DECK
        # =================================================================
        self.control_frame = tk.Frame(root, bg=self.colors["bg_dark"], pady=20, padx=25)
        self.control_frame.pack(fill="x")

        # URL Bar
        tk.Label(self.control_frame, text="TARGET URL INPUT:", font=("Consolas", 10, "bold"), 
                 bg=self.colors["bg_dark"], fg=self.colors["neon_cyan"]).pack(anchor="w", pady=(0,5))
        
        input_container = tk.Frame(self.control_frame, bg=self.colors["bg_dark"])
        input_container.pack(fill="x")

        self.url_entry = tk.Entry(input_container, font=("Consolas", 14), bg="#1a1a1a", fg="white", 
                                  insertbackground="white", relief="flat")
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), ipady=10)
        self.url_entry.insert(0, "https://super-boba-d1ef7b.netlify.app") 

        # --- BUTTONS (FIXED VISIBILITY) ---
        # We use Black text (fg="black") so it is visible on bright neon backgrounds
        self.scan_btn = tk.Button(input_container, text="▶ START SCAN", command=self.start_scan_thread,
                                  font=self.font_btn, 
                                  bg=self.colors["neon_green"], fg="black", # Black Text on Green
                                  activebackground="#00cc33", activeforeground="black",
                                  width=15, cursor="hand2")
        self.scan_btn.pack(side="left", padx=5)

        self.stop_btn = tk.Button(input_container, text="⏹ ABORT", command=self.stop_scan,
                                  font=self.font_btn, 
                                  bg=self.colors["neon_red"], fg="black", # Black Text on Red
                                  activebackground="#cc0000", activeforeground="black",
                                  width=12, state="disabled", cursor="hand2")
        self.stop_btn.pack(side="left", padx=5)

        # =================================================================
        # 3. DATA TABLE
        # =================================================================
        tk.Label(root, text="LIVE THREAT FEED", font=("Impact", 16), 
                 bg=self.colors["bg_dark"], fg="#444").pack(anchor="w", padx=25, pady=(30, 5))

        table_frame = tk.Frame(root, bg=self.colors["bg_dark"])
        table_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        columns = ("time", "threat", "target", "action", "reason")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Headers
        self.tree.heading("time", text="TIME", anchor="center")
        self.tree.heading("threat", text="THREAT TYPE", anchor="w")
        self.tree.heading("target", text="TARGET", anchor="w")
        self.tree.heading("action", text="STATUS", anchor="center")
        self.tree.heading("reason", text="DETAILS", anchor="w")

        self.tree.column("time", width=100, anchor="center")
        self.tree.column("threat", width=180, anchor="w")
        self.tree.column("target", width=220, anchor="w")
        self.tree.column("action", width=120, anchor="center")
        self.tree.column("reason", width=500, anchor="w")

        # Color Tags (Neon Style)
        self.tree.tag_configure("CRITICAL", foreground=self.colors["neon_red"], background="#1a0505")
        self.tree.tag_configure("WARNING", foreground=self.colors["neon_yellow"], background="#1a1a00")
        self.tree.tag_configure("INFO", foreground="#888", background="#0a0a0a")
        self.tree.tag_configure("SYSTEM", foreground=self.colors["neon_cyan"], background="#0a0a0a")

        self.browser_running = False

    # --- LOGIC ---
    def gui_callback(self, type, data):
        if type == "log":
            try:
                parts = data.split(":::")
                if len(parts) == 5:
                    level, threat, target, action, reason = parts
                    self.add_table_row(level, threat, target, action, reason)
            except: pass
        elif type == "score":
            self.update_score(data)

    def add_table_row(self, level, threat, target, action, reason):
        def _update():
            timestamp = time.strftime('%H:%M:%S')
            tag = "INFO"
            if "CRITICAL" in level: tag = "CRITICAL"
            elif "WARNING" in level: tag = "WARNING"
            elif "INFO" in level: tag = "SYSTEM"
            
            self.tree.insert("", 0, values=(timestamp, threat, target, action, reason), tags=(tag,))
        self.root.after_idle(_update)

    def update_score(self, score):
        def _update():
            color = self.colors["neon_green"]
            status = "(SECURE)"
            if score > 30: 
                color = self.colors["neon_yellow"]
                status = "(ELEVATED)"
            if score > 70: 
                color = self.colors["neon_red"]
                status = "(CRITICAL)"
            
            self.risk_val_label.config(text=f"{score}/100 {status}", fg=color)
        self.root.after_idle(_update)

    def start_scan_thread(self):
        url = self.url_entry.get()
        if not url: return
        self.browser_running = True
        self.scan_btn.config(state="disabled", bg="#333", fg="#555")
        self.stop_btn.config(state="normal", bg=self.colors["neon_red"], fg="black")
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.add_table_row("INFO", "System", "Agent", "INIT", "Defense Protocols Engaged...")

        threading.Thread(target=self.run_browser, args=(url,), daemon=True).start()

    def run_browser(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, args=["--start-maximized"])
            context = browser.new_context(no_viewport=True)
            page = context.new_page()

            guard = BrowserBodyguard(page, self.gui_callback)
            
            if not url.startswith("http"): url = "https://" + url
            try:
                page.goto(url)
                while self.browser_running:
                    guard.scan_page()
                    page.wait_for_timeout(2000)
            except: pass
            
            browser.close()
            self.stop_scan_gui_reset()

    def stop_scan(self):
        self.browser_running = False

    def stop_scan_gui_reset(self):
        def _reset():
            self.scan_btn.config(state="normal", bg=self.colors["neon_green"], fg="black")
            self.stop_btn.config(state="disabled", bg="#333", fg="#555")
            self.add_table_row("INFO", "System", "Agent", "STOP", "Session Terminated.")
        self.root.after_idle(_reset)

if __name__ == "__main__":
    root = tk.Tk()
    app = AegisDashboard(root)
    root.mainloop()
