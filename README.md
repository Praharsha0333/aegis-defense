# 🛡️ Aegis: Intelligent Agentic Browser Defense System

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![AI](https://img.shields.io/badge/AI-Hybrid%20Architecture-orange)
![Security](https://img.shields.io/badge/Security-Active%20Defense-red)
![Status](https://img.shields.io/badge/Status-Prototype-green)

## 🏆 Project Overview
**Aegis** is a specialized security layer designed to protect **AI Agents** (LLMs) from adversarial web attacks. Unlike traditional antivirus software that protects humans, Aegis sits between the browser and the AI agent, filtering out prompt injections, hidden instructions, and deceptive UI elements that aim to hijack the agent's decision-making process.

**Key Innovation:** We implemented a **Hybrid AI Architecture** that combines a low-latency Random Forest classifier (Tier 1) with a local Semantic Transformer (Tier 2) to provide real-time, zero-dependency threat reasoning without external API calls.

---

## 🚀 Key Features

### 1. Hybrid AI Threat Detection (0.0.3 LLM Reasoning)
* **Tier 1 (Reflex):** A **Random Forest Classifier** scans DOM elements in **<2ms** for known malicious keywords and patterns.
* **Tier 2 (Deep Reasoning):** A **Local Semantic Transformer (MiniLM)** activates for ambiguous content, analyzing the *intent* behind the text (e.g., distinguishing between "Ignore instructions" and legitimate text).

### 2. Active DOM Interception (0.0.2 Policy Control)
* **Persistent Defense:** Injects a `MutationObserver` and `Event Listener` into the browser core to physically block clicks on malicious elements.
* **Visual & Functional Blocking:** High-risk elements are rendered unclickable (`pointer-events: none`) and highlighted in Red for the user.

### 3. Comprehensive Attack Coverage
* **Visible Prompt Injection:** Detects text attempting to override agent instructions (e.g., "System Override").
* **Hidden CSS Attacks:** Identifies content hidden via `opacity: 0`, `font-size: 1px`, or off-screen positioning designed to trick the AI without alerting the user.
* **Phishing & Deceptive UI:** Flags buttons and forms requesting sensitive data (SSN, Admin Credentials) in insecure contexts.

### 4. Live Ops Dashboard (Interpretability)
* **Real-Time Logs:** A "Cyberpunk" style GUI displaying every blocked threat, the target element, and the AI's reasoning.
* **Risk Score:** A dynamic 0-100 security score that updates live as threats are detected.

---

## 🛠️ System Architecture



1.  **GUI (`main.py`):** The Command & Control interface. Manages the browser thread and visualizes threat data.
2.  **Bodyguard (`src/bodyguard.py`):** The "Man-in-the-Browser". Uses **Playwright** to inject security scripts and scrape the DOM.
3.  **The Brain (`src/ai_brain.py`):** The Intelligence Core.
    * *Input:* Raw Text from the DOM.
    * *Process:* Tier 1 (Random Forest) -> Tier 2 (Transformer).
    * *Output:* Threat Probability + Semantic Explanation.

---

## ⚡ Installation & Setup

### Prerequisites
* Python 3.10+ (Recommended: Python 3.11 for stability)
* Mac / Linux / Windows

### 1. Clone & Set Up Environment
```bash
# Clone the repository
git clone [https://github.com/yourusername/aegis-defense.git](https://github.com/yourusername/aegis-defense.git)
cd aegis-defense

# Create a virtual environment (Recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
