from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Initialize Llama 3.2 4B
llm = ChatOllama(model="llama3.2:latest", temperature=0.2)

# Standard conversational prompt. No tools, no complex JSON schemas.
answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert synthesizer. Identify the most standard, widely accepted information from the context. Ignore highly specific enterprise edge cases or platform-specific tutorials unless the user explicitly asks for them."),
    ("user", "Original Query: {query}\n\nResearch Data:\n{context}")
])

answer_chain = answer_prompt | llm | StrOutputParser()

def run_answering(state: dict):
    query = state["query"]
    past_steps = state.get("past_steps", [])
    
    print(f"--- DRAFTING ANSWER FOR: {query} ---")
    
    # Format all the research we gathered into a single string
    context_str = ""
    for step_query, result in past_steps:
        context_str += f"Search: {step_query}\nResults: {result}\n\n"
        
    try:
        # The LLM just reads the context and writes a response
        final_answer = answer_chain.invoke({
            "query": query,
            "context": context_str
        })
        print("✅ ANSWER DRAFTED")
        
    except Exception as e:
        print(f"❌ ANSWERING FAILED. Error: {e}")
        final_answer = "Error generating answer."
        
    return {"draft_answer": final_answer}