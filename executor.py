from langchain_community.tools.tavily_search import TavilySearchResults
from memory.faiss_store import add_to_faiss
from langchain_core.documents import Document
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the raw Tavily backend directly
search_backend = TavilySearchResults(max_results=3)

def run_executor(state: dict):
    plan = state.get("plan", [])
    print(f"--- EXECUTING PLAN: {len(plan)} steps ---")
    
    executed_steps = []
    
    for step in plan:
        print(f"🔍 Searching for: {step}")
        try:
            raw_results = search_backend.invoke({"query": step})
            
            # THE FIX: Stop dumping raw JSON. Extract ONLY the text content.
            # Tavily returns a list of dicts: [{'url': '...', 'content': '...'}]
            clean_snippets = []
            for result in raw_results:
                if "content" in result:
                    clean_snippets.append(result["content"])
            
            # Join the clean text together
            clean_context = "\n---\n".join(clean_snippets)
            
            # Save the clean text to FAISS
            doc = Document(page_content=clean_context, metadata={"source": "tavily", "query": step})
            add_to_faiss(doc)
            
            # Pass ONLY the clean text to the Answer Agent
            executed_steps.append((step, clean_context))
            
        except Exception as e:
            print(f"❌ Search failed for '{step}': {e}")
            executed_steps.append((step, f"Search failed: {e}"))
            
    return {"past_steps": executed_steps}