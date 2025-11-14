import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")
    
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


messages = [
    HumanMessage(content="Are u working? reply only Yes or No?"),
]
print("--- Messages passed to LLM for the next AI response ---")
for msg in messages:
    print(f"Type: {type(msg).__name__}, Content: {msg.content}")

ai_msg = llm.invoke(messages)

messages.append(ai_msg)

print("AI Response:", ai_msg)

print("\n--- Full Conversation History ---")
for msg in messages:
    print(type(msg).__name__)
    print(f"[{type(msg).__name__.replace('Message', '')}]: {msg.content}")