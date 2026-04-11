# 🛡️ Zero-Leak SOC Copilot

An enterprise-grade, multi-agent Threat Intelligence Copilot built with **LangGraph** and **Llama 3.2**. 

Designed for Security Operations Centers (SOC), this Copilot operates on a strict "Zero-Leak" architecture. It runs fully local LLMs to ensure sensitive corporate data never leaves the hardware, utilizes a dual-memory system for both ephemeral research and long-term corporate memory, and dynamically routes security queries to the appropriate external or internal tools.

## ✨ Key Features

* **Zero-Leak Privacy:** Hardcoded secrets and PII are automatically scrubbed via Microsoft Presidio before OSINT research begins. The core reasoning engine uses Llama 3.2 running locally via Ollama.
* **Agentic Routing:** A designated Planner Agent evaluates the user's input and dynamically routes execution to:
  * `VirusTotal API` for file hash analysis.
  * `Tavily API` for targeted OSINT web scraping (CVEs, threat actor campaigns).
  * `ChromaDB` for semantic search of internal corporate runbooks and historical incident logs.
* **Dual-Memory Architecture:** * **Short-Term (FAISS):** Acts as ephemeral working memory, holding live OSINT and API data for the duration of the current investigation.
  * **Long-Term (ChromaDB):** Acts as persistent corporate memory, retrieving historical incident tickets and internal playbooks.
* **Stateful Conversational UI:** Powered by LangGraph's state management, the Copilot remembers conversation history. It automatically generates a structured Markdown Dashboard for new incidents, and seamlessly transitions into a conversational chat format for follow-up questions.
* **Jailbreak Immunity:** Integrated with `Llama Guard` to intercept and block malicious prompts (e.g., requests to write exploit scripts) before they reach the reasoning engine.
* **RLHF Alignment Override:** Prompt-engineered to bypass standard AI hesitation filters, acting fully in-character as a Senior Network Security Engineer providing direct firewall port configurations and remediation advice.

## 🏗️ Architecture

1. **Streamlit UI:** Accepts user input (hashes, logs, questions).
2. **Llama Guard Node:** Scans for prompt injection or malicious intent.
3. **Planner Agent:** Synthesizes the objective into actionable steps (OSINT, API, or Vector DB).
4. **Executor Agent (Router):** Executes the plan using backend tools and stores findings in FAISS.
5. **Answer Agent:** Reads FAISS context + LangGraph `chat_history` to synthesize the final incident briefing.

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* [Ollama](https://ollama.com/) installed and running locally.
* API Keys for [Tavily](https://tavily.com/) and [VirusTotal](https://www.virustotal.com/).

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/zero-leak-soc-copilot.git](https://github.com/yourusername/zero-leak-soc-copilot.git)
   cd zero-leak-soc-copilot
   
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Pull the local models:**
   ```bash
   ollama pull llama3.2:4b

4. **Configure Environment Variables:**
  Create a .env file in the root directory:
   ```bash
   TAVILY_API_KEY=your_tavily_key_here
   VT_API_KEY=your_virustotal_key_here

5. **Initialize the Long-Term Memory (ChromaDB):**
  Run the database builder to ingest your dummy historical logs:
   ```bash
   python build_db.py

6. **Running the Application:**
  Ensure Ollama is running in the background (ollama serve), then launch the UI:
   ```bash
   streamlit run app.py

## 🧪 Testing Scenarios

* **API Routing:**Paste a file hash (e.g., `24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c`) to watch it trigger VirusTotal.
