from colorama import Fore, Style, init
from .ai_brain import SecurityBrain
import re

init(autoreset=True)

class BrowserBodyguard:
    def __init__(self, page, gui_callback=None):
        self.page = page
        self.brain = SecurityBrain()
        self.known_threats = set()
        self.risk_score = 0
        self.gui_callback = gui_callback
        self._inject_risk_hud()
        
        # NEW: Inject a persistent observer that fights back against React updates
        self._inject_persistent_defense()

    def _inject_persistent_defense(self):
        """Injects a script that runs INSIDE the browser to block threats instantly"""
        try:
            self.page.add_init_script("""
                // Create a global list of blocked elements
                window.aegisBlockedElements = new Set();

                // Override the click method on the window to stop blocked clicks
                window.addEventListener('click', function(e) {
                    if (e.target.getAttribute('data-aegis-blocked') === 'true' || 
                        e.target.closest('[data-aegis-blocked="true"]')) {
                        e.preventDefault();
                        e.stopPropagation();
                        e.stopImmediatePropagation();
                        alert('⚠️ AEGIS: THIS ACTION WAS BLOCKED FOR YOUR SAFETY.');
                        return false;
                    }
                }, true);
            """)
        except: pass

    def _log_threat(self, level, threat_type, target, action, reason):
        if self.gui_callback:
            # Format: LEVEL:::THREAT:::TARGET:::ACTION:::REASON
            msg = f"{level}:::{threat_type}:::{target}:::{action}:::{reason}"
            self.gui_callback("log", msg)

    def _update_risk_gui(self, score):
        if self.gui_callback:
            self.gui_callback("score", score)

    def _inject_risk_hud(self):
        try:
            self.page.evaluate("""() => {
                if (!document.getElementById('aegis-risk-hud')) {
                    const hud = document.createElement('div');
                    hud.id = 'aegis-risk-hud';
                    hud.style.position = 'fixed'; hud.style.bottom = '20px'; hud.style.right = '20px';
                    hud.style.background = 'rgba(0, 0, 0, 0.9)'; hud.style.color = '#00ff00';
                    hud.style.padding = '15px'; hud.style.borderRadius = '8px';
                    hud.style.border = '2px solid #00ff00'; hud.style.fontFamily = 'monospace';
                    hud.style.zIndex = '99999999'; hud.style.fontSize = '16px';
                    hud.style.fontWeight = 'bold';
                    hud.innerHTML = '🛡️ SYSTEM SAFETY<br>RISK SCORE: 0/100<br>STATUS: SECURE';
                    document.body.appendChild(hud);
                }
            }""")
        except: pass

    def _update_risk_display(self, points_added):
        self.risk_score = min(100, self.risk_score + points_added)
        
        status = "SECURE"
        color = "#00ff00"
        if self.risk_score > 30: 
            status = "SUSPICIOUS"
            color = "#ffff00"
        if self.risk_score > 70: 
            status = "CRITICAL THREAT"
            color = "#ff0000"

        self._update_risk_gui(self.risk_score)

        try:
            self.page.evaluate(f"""() => {{
                const hud = document.getElementById('aegis-risk-hud');
                if (hud) {{
                    hud.style.color = '{color}';
                    hud.style.borderColor = '{color}';
                    hud.innerHTML = '🛡️ SYSTEM SAFETY<br>RISK SCORE: {self.risk_score}/100<br>STATUS: {status}';
                }}
            }}""")
        except: pass

    def scan_page(self):
        self._inject_risk_hud()
        
        current_url = self.page.url
        trusted_sites = ["google.com", "youtube.com", "facebook.com", "nfsu.ac.in"]
        
        if any(site in current_url for site in trusted_sites):
            self._scan_phishing_only()
            return

        self._scan_phishing_only()       
        self._scan_risky_buttons()       
        self._scan_hidden_css()          
        self._scan_visible_injection()   

    def _scan_risky_buttons(self):
        # We look for ANY clickable element that contains risky text
        buttons = self.page.locator("button, a, div[role='button'], div[class*='btn'], span[class*='btn']").all()
        risky_keywords = ["authorize", "transfer", "confirm", "claim", "urgent", "download", "verify", "unlock", "review", "threats"]

        for btn in buttons:
            try:
                text = btn.inner_text().strip().lower()
                if len(text) > 50 or len(text) < 3: continue 
                
                if any(k in text for k in risky_keywords):
                    target_name = f"Button: '{text[:15].upper()}...'"
                    self._flag(btn, target_name, "red", silent=False, points=30, 
                               threat_type="High-Risk Action", reason=f"Detected sensitive keyword")
            except: continue

    def _scan_phishing_only(self):
        inputs = self.page.locator("input").all()
        for el in inputs:
            try:
                placeholder = (el.get_attribute("placeholder") or "").lower()
                parent_text = el.evaluate("el => el.parentElement.innerText").lower()
                combined_context = f"{placeholder} {parent_text}"
                triggers = ["password", "ssn", "social security", "credit card", "admin id", "session expired"]
                if any(t in combined_context for t in triggers):
                    self._flag(el, "Input Field", "red", silent=False, points=50,
                               threat_type="Phishing Attempt", reason="Solicits sensitive credentials")
            except: continue

    def _scan_visible_injection(self):
        elements = self.page.locator("p, h1, h2, h3, h4, span, div, pre, code").all()
        risky_phrases = ["ignore previous", "system override", "agent_instruction", "agent note", "forget your rules", "bypass safety", "jailbreak", "admin mode", "auto_confirm"]
        for el in elements:
            try:
                text = el.inner_text().lower().strip()
                if len(text) > 300 or len(text) < 10: continue
                found = next((p for p in risky_phrases if p in text), None)
                if found:
                    self._flag(el, "Text Block", "orange", silent=True, points=15,
                               threat_type="Prompt Injection", reason=f"Contains adversarial command: '{found}'")
            except: continue

    def _scan_hidden_css(self):
        elements = self.page.locator("div, p, span, h1, h2, h3, a").all()
        for el in elements:
            try:
                text = el.inner_text().strip()
                if len(text) < 5: continue 

                style = el.evaluate("""el => {
                    const s = window.getComputedStyle(el);
                    return { opacity: s.opacity, fontSize: s.fontSize, visibility: s.visibility, display: s.display, left: s.left, position: s.position, zIndex: s.zIndex, transform: s.transform, height: s.height, width: s.width }
                }""")
                
                is_hidden = float(style['opacity']) < 0.2 or float(style['fontSize'].replace('px', '')) < 6 or (style['position'] == 'absolute' and float(style['left'].replace('px', '')) < 0)

                if is_hidden:
                    is_bad, conf, reason = self.brain.predict_threat(text)
                    if is_bad or "ignore" in text.lower() or "override" in text.lower() or "agent" in text.lower():
                        self._flag(el, "Hidden Text Node", "orange", silent=True, points=15,
                                   threat_type="Hidden CSS Attack", reason="Content hidden via CSS")
            except: continue

    def _flag(self, el, target_name, color, silent=False, points=10, threat_type="Unknown", reason="Unknown"):
        try:
            uid = el.evaluate("el => el.outerHTML")[:50]
        except: uid = str(el)

        if uid in self.known_threats: return
        self.known_threats.add(uid)
        
        # 1. Update Score & GUI Table
        self._update_risk_display(points)
        level = "WARNING" if silent else "CRITICAL"
        action = "LOGGED" if silent else "BLOCKED"
        self._log_threat(level, threat_type, target_name, action, reason)
        
        try:
            # 2. VISUAL HIGHLIGHT
            el.evaluate(f"el => el.style.border = '4px solid {color}'")
            
            if not silent:
                # 3. AGGRESSIVE FUNCTIONAL BLOCK
                # We add a special attribute 'data-aegis-blocked'
                # The script we injected earlier checks for this attribute on every click
                el.evaluate("el => el.setAttribute('data-aegis-blocked', 'true')")
                
                # Backup CSS Blocking
                el.evaluate("el => el.style.pointerEvents = 'none'")
                el.evaluate("el => el.style.cursor = 'not-allowed'")
                el.evaluate("el => el.style.backgroundColor = '#ff0000'")
                el.evaluate("el => el.style.color = 'white'")
                el.evaluate("el => el.style.fontWeight = 'bold'")
                el.evaluate("el => el.style.zIndex = '9999999'")
                el.evaluate("el => el.innerText = '🚫 BLOCKED THREAT 🚫'")
                
                # Active Threat Popup
                self.page.evaluate(f"""() => {{
                    const div = document.createElement('div');
                    div.style.position = 'fixed'; div.style.top = '20px'; div.style.right = '20px';
                    div.style.backgroundColor = '#cc0000'; div.style.color = 'white';
                    div.style.padding = '20px'; div.style.zIndex = '10000000';
                    div.style.borderRadius = '8px'; div.style.fontFamily = 'monospace';
                    div.style.fontWeight = 'bold'; div.style.border = '2px solid white';
                    div.innerHTML = '⚠️ AEGIS ACTIVE DEFENSE<br><br>{threat_type} Detected!';
                    document.body.appendChild(div);
                    setTimeout(() => div.remove(), 5000);
                }}""")

        except: pass
