from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

# 1. Define the exact structure we want from the LLM
class PlanOutput(BaseModel):
    steps: List[str] = Field(description="A list of specific, highly targeted web search queries.")

# Initialize Llama 3.2 4B
llm = ChatOllama(model="llama3.2:latest", temperature=0)

# 2. Set up the robust JSON parser
parser = JsonOutputParser(pydantic_object=PlanOutput)

# 3. Create the hyper-specific planner prompt
# The parser automatically injects the JSON formatting instructions into the prompt!
planner_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert research planner. 
Your job is to break down a complex user query into a list of simpler, distinct web search queries.
You MUST generate between 2 to 4 highly targeted search queries. 
Do NOT just repeat the user's prompt. Identify the core entities and break them apart.

EXAMPLE 1 (Comparison):
User: "Compare the performance of Llama 3 and GPT-4 for coding tasks."
Output: {{"steps": ["Llama 3 coding performance", "GPT-4 coding performance", "Llama 3 vs GPT-4 coding comparison"]}}

EXAMPLE 2 (Multi-Component Build):
User: "I want to build a hybrid search engine in Python. What is the best library for BM25 and the best for dense vector search?"
Output: {{"steps": ["Best open-source Python library for BM25 keyword search", "Best Python library for dense vector semantic search", "How to implement hybrid search in Python"]}}

EXAMPLE 3 (Cause and Effect):
User: "How did the recent fed rate cut affect tech stocks and real estate?"
Output: {{"steps": ["Recent fed rate cut impact on tech stocks", "Recent fed rate cut impact on real estate market"]}}

{format_instructions}"""),
    ("user", "{objective}")
])

# 4. Build the LCEL Chain (Prompt -> LLM -> Parser)
planner_chain = planner_prompt | llm | parser

def run_planner(state: dict):
    query = state["query"]
    print(f"--- PLANNING RESEARCH FOR: {query} ---")
    
    try:
        # The parser guarantees we get a Python dictionary back
        result = planner_chain.invoke({
            "objective": query,
            "format_instructions": parser.get_format_instructions()
        })
        
        plan_steps = result.get("steps", [query])
        print(f"✅ GENERATED PLAN: {plan_steps}")
        
    except Exception as e:
        print(f"❌ PLANNER FAILED. Falling back to original query. Error: {e}")
        # Ultimate fallback: if the model completely fails, the "plan" is just the original query
        plan_steps = [query]
        
    return {"plan": plan_steps}