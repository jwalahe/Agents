import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
from Agents.ReAct.WikiTool import WikiTool
from Agents.ReAct.promptTemplate import SYSTEM, EXAMPLES
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_action(text):
    # Simple parser to extract search or lookup and query
    
    # Looks for Action 1: search["..."] or lookup["..."]
    match = re.search(r'Action\s*\d*:\s*(search|lookup)\["([^"]+)"\]', text)
    if match:
        return match.group(1), match.group(2)
    else:
        return None, None

def run_react_loop(question):
    wiki_tool = WikiTool()
    history = f"{SYSTEM}\n{EXAMPLES}\n# New Question\nQuestion: {question}"
    observation_count = 0
    
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": history}],
            temperature=0.0
        )
        content = response.choices[0].message.content.strip()
        print("AI:", content)
        
        if content.startswith("Action"):
            observation_count += 1
            action_type, action_query = parse_action(content)
            if action_type == "search":
                obs = wiki_tool.search(action_query)
            elif action_type == "lookup":
                obs = wiki_tool.lookup(page=action_query)
            else:
                obs = "Invalid action. Please use search[\"query\"] or lookup[\"page\"]."
            history += f"\n{content}\nObservation {observation_count}: {obs}"
        elif content.startswith("Thought"):
            history += f"\n{content}"
        elif content.startswith("Final Answer"):
            print("\nFinal Answer:", content.replace("Final Answer:", "").strip())
            break
        else:
            history += f"\n{content}"
            # Continue the loop to let the model correct itself

if __name__ == "__main__":
    question = input("Enter your HotpotQA-style question: ")
    run_react_loop(question)
