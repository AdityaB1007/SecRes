import streamlit as st
from graph import app  

st.set_page_config(page_title="Agentic Research Assistant", page_icon="🤖", layout="centered")

st.title("Deterministic Agentic RAG")
st.markdown("Powered by Llama 3.2 4B (Plan-and-Execute Architecture)")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Catch user input
if prompt := st.chat_input("Ask a complex research question..."):
    
    # 1. Display and save the user's prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Setup the Assistant's response area
    with st.chat_message("assistant"):
        final_answer = ""
        
        with st.status("Initializing Plan-and-Execute Graph...", expanded=True) as status:
            
            inputs = {"query": prompt, "past_steps": []}
            
            for output in app.stream(inputs):
                for node_name, node_state in output.items():
                    
                    if node_name == "guard":
                        if node_state.get("is_safe") == False:
                            st.error("🛑 **Security Guardrail Triggered:** Request blocked.")
                            final_answer = node_state.get("draft_answer")
                            
                    elif node_name == "planner":
                        plan = node_state.get("plan", [])
                        st.write(f"🧠 **Phase 1 (Planner):** Generated {len(plan)} search tasks.")
                        # Use st.json instead of an expander to show the list cleanly
                        st.json(plan)
                            
                    elif node_name == "executor":
                        past_steps = node_state.get("past_steps", [])
                        st.write(f"⚡ **Phase 2 (Executor):** Successfully retrieved web context.")
                        # Write the search details directly into the status block
                        for search_query, result in past_steps:
                            st.markdown(f"**Searched:** `{search_query}`")
                            st.caption(f"{result[:300]}...") 
                            st.divider()
                                
                    elif node_name == "answer":
                        st.write("✍️ **Phase 3 (Synthesizer):** Drafting final response.")
                        final_answer = node_state.get("draft_answer", "Error drafting answer.")
            
            # This collapses the status box when finished, hiding all the raw data
            status.update(label="Research Complete!", state="complete", expanded=False)
        
        # 3. Output the final generated response OUTSIDE the status box
        st.markdown(final_answer)
        
        st.session_state.messages.append({"role": "assistant", "content": final_answer})