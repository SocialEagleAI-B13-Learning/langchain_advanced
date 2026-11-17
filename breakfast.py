import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# 1. Setup API key and model
os.environ["OPENAI_API_KEY"] = "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"
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 2. Prompt Template using a placeholder for our clean history list
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, witty culinary assistant. You remember all previously discussed recipes and context."),
    ("placeholder", "{chat_history}"),
    ("user", "{input}")
])

# 3. Build the chain
chain = prompt | model | StrOutputParser()

# 4. Standard Python list to hold conversation history
chat_history = []

print("=== Interactive Culinary Assistant (Warning-Free!) ===")
print("Type any food item or question (Type 'exit' to quit).\n")

# 5. Interactive Loop
while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("\nAI: Happy cooking! Goodbye!")
        break
    
    print("AI: ", end="", flush=True)
    
    # Stream the response using current input and history list
    response_text = ""
    for chunk in chain.stream({"input": user_input, "chat_history": chat_history}):
        print(chunk, end="", flush=True)
        response_text += chunk
        
    print("\n" + "-" * 50)
    
    # Manually update history after the turn is complete
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response_text))