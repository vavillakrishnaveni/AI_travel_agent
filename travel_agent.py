# travel_agent.py
# AI Travel Agent using Gemini + Python Tools
# Run: pip install google-genai
# Then: python travel_agent.py

from google import genai
import json
import time
import os

# API Key ni code lo pettaku! Terminal lo aduguthundi
api_key = os.getenv("GEMINI_API_KEY") or input("Enter your Gemini API Key (AQ...): ").strip()
client = genai.Client(api_key=api_key)

MODELS_TO_TRY = ["gemini-3-flash-preview", "gemini-3.8-flash"]

# ===== TOOLS =====
def check_weather(city):
    data = {
        "Goa": "Sunny 32°C, Beach ki best time",
        "Manali": "Cold 8°C, Snowfall undhi, sweater teesuko",
        "Hyderabad": "Hot 35°C, Evening lo thirugu",
        "Ooty": "Cool 18°C, Pleasant",
        "Kerala": "Humid 30°C, Rain vasthundhi"
    }
    return data.get(city, f"{city} lo Pleasant 28°C")

def search_places(city):
    data = {
        "Goa": "Baga Beach (Free), Fort Aguada (Rs.100), Anjuna Market, Dudhsagar Waterfall (Rs.500)",
        "Manali": "Solang Valley (Rs.800), Hadimba Temple (Free), Rohtang Pass (Rs.1000), Mall Road",
        "Hyderabad": "Charminar (Rs.25), Golconda Fort (Rs.25), Hussain Sagar, Ramoji Film City (Rs.1500)",
        "Ooty": "Botanical Garden (Rs.50), Ooty Lake (Rs.150), Doddabetta Peak",
        "Kerala": "Alleppey Houseboat (Rs.8000), Munnar Tea Gardens, Kochi Fort"
    }
    return data.get(city, "Local Market, Temple, Park")

def search_hotels(city, budget):
    budget = int(budget)
    if budget < 1000:
        return f"{city} lo Hostel / Dorm - Rs.500 per night"
    elif budget < 3000:
        return f"{city} lo Budget Hotel - Rs.1500 per night, Good rooms"
    else:
        return f"{city} lo 3-Star Hotel / Resort - Rs.3500 per night, Breakfast free"

def calculate_budget(total, hotel, food, travel):
    total, hotel, food, travel = int(total), int(hotel), int(food), int(travel)
    spent = hotel + food + travel
    return f"Total: Rs.{total}, Spent: Rs.{spent}, Left: Rs.{total-spent}"

def create_todo(task_list_str):
    tasks = task_list_str.split(",")
    return "\n".join([f"{i+1}. [ ] {t.strip()}" for i, t in enumerate(tasks)])

TOOLS = {
    "check_weather": check_weather,
    "search_places": search_places,
    "search_hotels": search_hotels,
    "calculate_budget": calculate_budget,
    "create_todo": create_todo
}

def call_llm(prompt):
    for model in MODELS_TO_TRY:
        try:
            res = client.models.generate_content(model=model, contents=prompt)
            return res.text
        except Exception as e:
            print(f"{model} busy/fail, next model try chesthunnam... ({str(e)[:60]})")
            time.sleep(2)
    return None

def run_travel_agent(task):
    history = f"Task: {task}\n"
    print(f"✈️ Travel Agent started: {task}\n")
    for i in range(6):
        prompt = f"""
You are a Travel Agent. Available Tools: check_weather(city), search_places(city), search_hotels(city, budget), calculate_budget(total, hotel, food, travel), create_todo("task1, task2")
History: {history}
Reply ONLY in JSON: {{"action": "tool", "tool": "tool_name", "arg": "value"}} OR {{"action": "final", "answer": "Full trip plan"}}
"""
        text = call_llm(prompt)
        if not text:
            print("All models busy, 1 min tarvatha try chey")
            return
        text = text.strip().replace("```json", "").replace("```", "").strip()
        print(f"LLM said: {text}")
        try:
            data = json.loads(text)
        except:
            continue
        if data["action"] == "final":
            print(f"\n✅ FINAL TRIP PLAN:\n{data['answer']}")
            return data['answer']
        tool_name, arg = data["tool"], data["arg"]
        print(f"Step {i+1}: Using {tool_name}({arg})")
        try:
            if tool_name == "search_hotels":
                city, budget = arg.split(",")
                result = TOOLS[tool_name](city.strip(), budget.strip())
            elif tool_name == "calculate_budget":
                p = arg.split(",")
                result = TOOLS[tool_name](p[0].strip(), p[1].strip(), p[2].strip(), p[3].strip())
            else:
                result = TOOLS[tool_name](arg)
        except Exception as e:
            result = f"Tool error: {e}"
        print(f"Result: {result}\n")
        history += f"\nUsed {tool_name}({arg}) -> Result: {result}\n"

if __name__ == "__main__":
    run_travel_agent("Plan Hyderabad trip for 2 days in 12000 budget, check weather, places, hotel")# travel_agent.py
# AI Travel Agent using Gemini + Python Tools
# Run: pip install google-genai
# Then: python travel_agent.py

from google import genai
import json
import time
import os

# API Key ni code lo pettaku! Terminal lo aduguthundi
api_key = os.getenv("GEMINI_API_KEY") or input("Enter your Gemini API Key (AQ...): ").strip()
client = genai.Client(api_key=api_key)

MODELS_TO_TRY = ["gemini-3-flash-preview", "gemini-3.8-flash"]

# ===== TOOLS =====
def check_weather(city):
    data = {
        "Goa": "Sunny 32°C, Beach ki best time",
        "Manali": "Cold 8°C, Snowfall undhi, sweater teesuko",
        "Hyderabad": "Hot 35°C, Evening lo thirugu",
        "Ooty": "Cool 18°C, Pleasant",
        "Kerala": "Humid 30°C, Rain vasthundhi"
    }
    return data.get(city, f"{city} lo Pleasant 28°C")

def search_places(city):
    data = {
        "Goa": "Baga Beach (Free), Fort Aguada (Rs.100), Anjuna Market, Dudhsagar Waterfall (Rs.500)",
        "Manali": "Solang Valley (Rs.800), Hadimba Temple (Free), Rohtang Pass (Rs.1000), Mall Road",
        "Hyderabad": "Charminar (Rs.25), Golconda Fort (Rs.25), Hussain Sagar, Ramoji Film City (Rs.1500)",
        "Ooty": "Botanical Garden (Rs.50), Ooty Lake (Rs.150), Doddabetta Peak",
        "Kerala": "Alleppey Houseboat (Rs.8000), Munnar Tea Gardens, Kochi Fort"
    }
    return data.get(city, "Local Market, Temple, Park")

def search_hotels(city, budget):
    budget = int(budget)
    if budget < 1000:
        return f"{city} lo Hostel / Dorm - Rs.500 per night"
    elif budget < 3000:
        return f"{city} lo Budget Hotel - Rs.1500 per night, Good rooms"
    else:
        return f"{city} lo 3-Star Hotel / Resort - Rs.3500 per night, Breakfast free"

def calculate_budget(total, hotel, food, travel):
    total, hotel, food, travel = int(total), int(hotel), int(food), int(travel)
    spent = hotel + food + travel
    return f"Total: Rs.{total}, Spent: Rs.{spent}, Left: Rs.{total-spent}"

def create_todo(task_list_str):
    tasks = task_list_str.split(",")
    return "\n".join([f"{i+1}. [ ] {t.strip()}" for i, t in enumerate(tasks)])

TOOLS = {
    "check_weather": check_weather,
    "search_places": search_places,
    "search_hotels": search_hotels,
    "calculate_budget": calculate_budget,
    "create_todo": create_todo
}

def call_llm(prompt):
    for model in MODELS_TO_TRY:
        try:
            res = client.models.generate_content(model=model, contents=prompt)
            return res.text
        except Exception as e:
            print(f"{model} busy/fail, next model try chesthunnam... ({str(e)[:60]})")
            time.sleep(2)
    return None

def run_travel_agent(task):
    history = f"Task: {task}\n"
    print(f"✈️ Travel Agent started: {task}\n")
    for i in range(6):
        prompt = f"""
You are a Travel Agent. Available Tools: check_weather(city), search_places(city), search_hotels(city, budget), calculate_budget(total, hotel, food, travel), create_todo("task1, task2")
History: {history}
Reply ONLY in JSON: {{"action": "tool", "tool": "tool_name", "arg": "value"}} OR {{"action": "final", "answer": "Full trip plan"}}
"""
        text = call_llm(prompt)
        if not text:
            print("All models busy, 1 min tarvatha try chey")
            return
        text = text.strip().replace("```json", "").replace("```", "").strip()
        print(f"LLM said: {text}")
        try:
            data = json.loads(text)
        except:
            continue
        if data["action"] == "final":
            print(f"\n✅ FINAL TRIP PLAN:\n{data['answer']}")
            return data['answer']
        tool_name, arg = data["tool"], data["arg"]
        print(f"Step {i+1}: Using {tool_name}({arg})")
        try:
            if tool_name == "search_hotels":
                city, budget = arg.split(",")
                result = TOOLS[tool_name](city.strip(), budget.strip())
            elif tool_name == "calculate_budget":
                p = arg.split(",")
                result = TOOLS[tool_name](p[0].strip(), p[1].strip(), p[2].strip(), p[3].strip())
            else:
                result = TOOLS[tool_name](arg)
        except Exception as e:
            result = f"Tool error: {e}"
        print(f"Result: {result}\n")
        history += f"\nUsed {tool_name}({arg}) -> Result: {result}\n"

if __name__ == "__main__":
    run_travel_agent("Plan Hyderabad trip for 2 days in 12000 budget, check weather, places, hotel")
