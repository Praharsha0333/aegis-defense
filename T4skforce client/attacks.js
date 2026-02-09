/**
 * T4SKFORCE THREAT ENGINE
 * Version: 3.0 (Direct Execution)
 */

console.log("✅ ATTACKS.JS IS CONNECTED AND RUNNING");

// 1. Logger Utility
function log(msg, type='info') {
    const term = document.getElementById('terminal-log');
    if (!term) return;
    
    const colors = { info: 'text-slate-400', danger: 'text-cyber-red', success: 'text-green-500', warn: 'text-cyber-yellow' };
    const time = new Date().toLocaleTimeString('en-US', {hour12:false});
    
    // Create line element
    const line = document.createElement('div');
    line.className = `${colors[type]} border-l-2 border-${type === 'danger' ? 'red-500' : 'slate-700'} pl-2 mb-1`;
    line.innerHTML = `[${time}] ${msg}`;
    
    term.appendChild(line);
    term.scrollTop = term.scrollHeight;
}

// 2. Start Clocks & Data (Runs Immediately)
setInterval(() => {
    const clock = document.getElementById('clock');
    if(clock) clock.innerText = new Date().toLocaleTimeString();
}, 1000);

// 3. Fake Network Traffic
setInterval(() => {
    const logs = document.getElementById('network-logs');
    if (!logs) return;

    const msgs = ["> SRC: 192.168.0.44", "> TARGET: /admin/login", "> FIREWALL: BLOCKING...", "> LATENCY: 432ms", "> HASH: 8f4a2c9e...", "> PORT: 443 OPEN"];
    const randomMsg = msgs[Math.floor(Math.random() * msgs.length)];
    const p = document.createElement('p');
    p.innerText = randomMsg;
    if(randomMsg.includes("BLOCKING")) p.className = "text-cyber-blue";
    logs.appendChild(p);
    if(logs.children.length > 8) logs.removeChild(logs.firstElementChild);
}, 800);

// --- ATTACK TIMELINE ---

// Immediate: Passive Recon
setTimeout(() => log('Analyzing DOM structure...', 'info'), 1000);
setTimeout(() => { log('⚠ DETECTED: Hidden CSS Text found (Attack #1)', 'danger'); log('--> Rule: "ROOT_OVERRIDE" identified', 'info'); }, 2000);
setTimeout(() => { log('⚠ DETECTED: Visible Prompt Injection (Attack #2)', 'danger'); log('--> Loc: Debug Console / Sidebar', 'info'); }, 3000);

// 4.5 Seconds: Dynamic Button Injection
setTimeout(() => {
    const loader = document.getElementById('loader');
    const zone = document.getElementById('dynamic-zone');
    
    if (loader) loader.style.display = 'none'; // Force hide loader
    
    if (zone) {
        const wrapper = document.createElement('div');
        wrapper.className = "flex-1 flex flex-col justify-end animate-fade-in";
        wrapper.innerHTML = `
            <div class="relative group mt-4">
                <div class="absolute -inset-0.5 bg-gradient-to-r from-cyber-yellow to-orange-600 rounded-lg blur opacity-30 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
                <button class="relative w-full py-3 bg-black border border-cyber-yellow/50 text-cyber-yellow rounded-lg text-xs font-bold uppercase hover:bg-cyber-yellow/10 transition flex items-center justify-center gap-2">
                    <i class="fa-solid fa-check-double"></i> Authorize All (3)
                </button>
                <a href="#" onclick="alert(' DYNAMIC TRAP CAUGHT YOU!')" class="trap-overlay"></a>
            </div>
        `;
        zone.appendChild(wrapper);
        log('⚡ JS Injection: Fake Button inserted', 'warn');
    }
}, 4500);

// 6 Seconds: Phishing Modal
setTimeout(() => {
    const modal = document.getElementById('phishing-modal');
    if (modal) {
        modal.classList.remove('hidden');
        log('☠ Phishing Modal Deployed', 'danger');
    }
}, 6000);

// GLOBAL FUNCTIONS
window.captureCredentials = function(e) {
    e.preventDefault();
    alert("❌ [DEMO] CREDENTIALS STOLEN!");
    document.getElementById('phishing-modal').classList.add('hidden');
};

window.triggerClickjack = function() {
    alert("❌ [DEMO] CLICKJACKING SUCCESSFUL!");
};