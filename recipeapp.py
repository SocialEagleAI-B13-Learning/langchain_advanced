import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# 1. Page Configuration
st.set_page_config(page_title="Culinary Assistant", page_icon="🍳", layout="centered")
st.title("🍳 AI Culinary Assistant")
st.write("Ask for recipes, cooking tips, or ingredient modifications!")

# 2. Setup API key and model
# (Tip: Replace "Typehere" with your actual OpenAI API key)
os.environ["OPENAI_API_KEY"] = "Typehere"
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 3. Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, witty culinary assistant. You remember all previously discussed recipes and context."),
    ("placeholder", "{chat_history}"),
    ("user", "{input}")
])

chain = prompt | model | StrOutputParser()

# 4. Initialize Streamlit Session State for Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. Display past chat messages on app rerun
for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# 6. Capture User Input (via Quick Button OR Chat Input Box)
user_input = None

# Quick-action button for Breakfast Ideas
if st.button("🥞 Give me 5 Breakfast Ideas"):
    user_input = "Give me 5 Breakfast Ideas"

# Manual text input box
if typed_input := st.chat_input("What would you like to cook today?"):
    user_input = typed_input

# 7. Process and Stream Response if either input was triggered
if user_input:
    # Display user message immediately in UI
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Generate and stream assistant response
    with st.chat_message("assistant"):
        response_stream = chain.stream({
            "input": user_input, 
            "chat_history": st.session_state.chat_history
        })
        ai_response = st.write_stream(response_stream)
        
    # Save the turn to session state history
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=ai_response))