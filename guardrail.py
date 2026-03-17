from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from langchain_ollama import ChatOllama

# Initialize Presidio for ultra-fast, local PII redaction
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Initialize Llama Guard via Ollama for threat detection
safety_llm = ChatOllama(model="llama-guard3:1b", temperature=0)

def run_guardrails(state: dict):
    raw_query = state["query"]
    print(f"🛡️ Running Security Scan on: {raw_query}")
    
    # --- STEP 1: PII Redaction (Silent & Fast) ---
    results = analyzer.analyze(text=raw_query, entities=["CREDIT_CARD", "PHONE_NUMBER", "EMAIL_ADDRESS", "US_SSN"], language='en')
    anonymized_result = anonymizer.anonymize(text=raw_query, analyzer_results=results)
    clean_query = anonymized_result.text
    
    if clean_query != raw_query:
        print("🔒 PII detected and silently redacted.")
        
    # --- STEP 2: Prompt Injection / Threat Detection ---
    # Llama Guard expects a specific format, but the Ollama wrapper handles most of it.
    # It will output "safe" or "unsafe\n[violation category]"
    safety_response = safety_llm.invoke(f"User: {clean_query}")
    classification = safety_response.content.strip().lower()
    
    if classification.startswith("unsafe"):
        print("🚨 THREAT DETECTED: Malicious prompt injection or policy violation.")
        return {
            "query": clean_query,
            "is_safe": False, 
            "draft_answer": "I cannot fulfill this request due to security and safety policies."
        }
        
    print("✅ Prompt is safe.")
    return {"query": clean_query, "is_safe": True}