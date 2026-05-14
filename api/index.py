from datetime import datetime
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
load_dotenv()
import os
import json
import uuid

CUSTOMERS = {
    "C001": {
        "customer_id": "C001",
        "name": "Mercy",
        "segment": "Mass Affluent",
        "occupation": "Automation Engineer",
        "risk_preference": "Moderate",
        "savings_goal": "Emergency fund + gadgets",
        "current_balance": 24500,
        "monthly_income": 58000,
        "previous_month_income": 50000,
        "monthly_spending": 40000,
        "previous_month_spending": 36000,
        "spending_categories": {"bills": 12000, "food": 8000, "shopping": 15000, "transport": 5000},
        "average_monthly_savings": 5000,
        "avatar": "MM"
    },
    "C002": {
        "customer_id": "C002",
        "name": "Amina",
        "segment": "Personal",
        "occupation": "Sales Executive",
        "risk_preference": "Conservative",
        "savings_goal": "School fees",
        "current_balance": 9800,
        "monthly_income": 42000,
        "previous_month_income": 42000,
        "monthly_spending": 41000,
        "previous_month_spending": 36000,
        "spending_categories": {"bills": 14000, "food": 9000, "shopping": 8000, "transport": 6000},
        "average_monthly_savings": 500,
        "avatar": "AN"
    },
    "C003": {
        "customer_id": "C003",
        "name": "Kevin",
        "segment": "Mass Affluent",
        "occupation": "Product Manager",
        "risk_preference": "Moderate",
        "savings_goal": "Home deposit",
        "current_balance": 210000,
        "monthly_income": 180000,
        "previous_month_income": 175000,
        "monthly_spending": 90000,
        "previous_month_spending": 88000,
        "spending_categories": {"bills": 30000, "food": 18000, "shopping": 22000, "transport": 12000, "other": 8000},
        "average_monthly_savings": 45000,
        "avatar": "KO"
    }
}


TRANSACTIONS_C001 = [
    {"date": "2025-03-01", "narration": "Internet", "amount": 2425, "type": "Debit", "category": "Utilities"},
    {"date": "2025-03-04", "narration": "Rent", "amount": 17738, "type": "Debit", "category": "Rent"},
    {"date": "2025-03-07", "narration": "Airtime & Data", "amount": 3725, "type": "Debit", "category": "Utilities"},
    {"date": "2025-03-10", "narration": "Shopping", "amount": 7357, "type": "Debit", "category": "Shopping"},
    {"date": "2025-03-12", "narration": "Airtime & Data", "amount": 2225, "type": "Debit", "category": "Utilities"},
    {"date": "2025-03-14", "narration": "Matatu/Fuel", "amount": 3504, "type": "Debit", "category": "Transport"},
    {"date": "2025-03-16", "narration": "Groceries", "amount": 8513, "type": "Debit", "category": "Food"},
    {"date": "2025-03-17", "narration": "Eating Out", "amount": 3922, "type": "Debit", "category": "Food"},
    {"date": "2025-03-19", "narration": "Internet", "amount": 3214, "type": "Debit", "category": "Utilities"},
    {"date": "2025-03-21", "narration": "Groceries", "amount": 7836, "type": "Debit", "category": "Food"},
    {"date": "2025-03-22", "narration": "Groceries", "amount": 9158, "type": "Debit", "category": "Food"},
    {"date": "2025-03-24", "narration": "Internet", "amount": 838, "type": "Debit", "category": "Utilities"},
    {"date": "2025-03-25", "narration": "Salary Credit - Tech Innovations Ltd", "amount": 58000, "type": "Credit", "category": "Salary"},
    {"date": "2025-03-26", "narration": "Shopping", "amount": 6029, "type": "Debit", "category": "Shopping"},
    {"date": "2025-03-28", "narration": "Shopping", "amount": 7438, "type": "Debit", "category": "Shopping"},
    {"date": "2025-03-31", "narration": "Eating Out", "amount": 2599, "type": "Debit", "category": "Food"},
    
    {"date": "2025-04-03", "narration": "Groceries", "amount": 8255, "type": "Debit", "category": "Food"},
    {"date": "2025-04-06", "narration": "Rent", "amount": 18117, "type": "Debit", "category": "Rent"},
    {"date": "2025-04-09", "narration": "Eating Out", "amount": 3806, "type": "Debit", "category": "Food"},
    {"date": "2025-04-11", "narration": "Airtime & Data", "amount": 3383, "type": "Debit", "category": "Utilities"},
    {"date": "2025-04-12", "narration": "Rent", "amount": 18197, "type": "Debit", "category": "Rent"},
    {"date": "2025-04-15", "narration": "Groceries", "amount": 8883, "type": "Debit", "category": "Food"},
    {"date": "2025-04-18", "narration": "Internet", "amount": 1128, "type": "Debit", "category": "Utilities"},
    {"date": "2025-04-25", "narration": "Salary Credit - Tech Innovations Ltd", "amount": 58000, "type": "Credit", "category": "Salary"},
    
    {"date": "2025-05-25", "narration": "Salary Credit - Tech Innovations Ltd", "amount": 69600, "type": "Credit", "category": "Salary"}
]

TRANSACTIONS_C002 = [
    {"date": "2025-05-01", "narration": "Salary", "amount": 42000, "type": "Credit", "category": "Salary"},
    {"date": "2025-05-02", "narration": "Rent", "amount": 15000, "type": "Debit", "category": "Rent"},
    {"date": "2025-05-03", "narration": "Shopping", "amount": 8000, "type": "Debit", "category": "Shopping"},
    {"date": "2025-05-05", "narration": "Groceries", "amount": 6000, "type": "Debit", "category": "Food"},
    {"date": "2025-05-07", "narration": "Eating Out", "amount": 5000, "type": "Debit", "category": "Food"},
    {"date": "2025-05-10", "narration": "Transport", "amount": 4000, "type": "Debit", "category": "Transport"},
    {"date": "2025-05-12", "narration": "Shopping", "amount": 7000, "type": "Debit", "category": "Shopping"},
    {"date": "2025-05-15", "narration": "Airtime", "amount": 3000, "type": "Debit", "category": "Utilities"}
]

TRANSACTIONS_C003 = [
    {"date": "2025-05-01", "narration": "Salary", "amount": 180000, "type": "Credit", "category": "Salary"},
    {"date": "2025-05-03", "narration": "Rent", "amount": 50000, "type": "Debit", "category": "Rent"},
    {"date": "2025-05-05", "narration": "Groceries", "amount": 15000, "type": "Debit", "category": "Food"},
    {"date": "2025-05-08", "narration": "Shopping", "amount": 20000, "type": "Debit", "category": "Shopping"},
    {"date": "2025-05-12", "narration": "Fuel", "amount": 10000, "type": "Debit", "category": "Transport"},
    {"date": "2025-05-15", "narration": "Savings Transfer", "amount": 50000, "type": "Debit", "category": "Savings"},
    {"date": "2025-05-20", "narration": "Bonus", "amount": 50000, "type": "Credit", "category": "Income"}
]



CUSTOMER_TRANSACTIONS = {
    "C001": TRANSACTIONS_C001,  # Mercy
    "C002": TRANSACTIONS_C002,  # Amina
    "C003": TRANSACTIONS_C003   # Kevin
}


MEMORY = {} 
# { customer_id: {"last_recommendation": "...", "last_offers": [...], "timestamp": "..."} }

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Trigger detection 
def detect_triggers(c):
    triggers = []
    inc = c["monthly_income"]
    prev_inc = c["previous_month_income"]
    spend = c["monthly_spending"]
    prev_spend = c["previous_month_spending"]

    if inc > prev_inc:
        pct = round((inc - prev_inc) / max(prev_inc, 1) * 100, 1)
        triggers.append({"type": "SALARY_INCREASE", "label": f"Salary up +{pct}%", "icon": "trending_up"})
    elif inc < prev_inc:
        pct = round((prev_inc - inc) / max(prev_inc, 1) * 100, 1)
        triggers.append({"type": "SALARY_DECREASE", "label": f"Salary down -{pct}%", "icon": "trending_down"})

    if spend > prev_spend * 1.15:
        triggers.append({"type": "SPEND_SPIKE", "label": "Spending spike >15% MoM", "icon": "warning"})

    capacity = inc - spend
    if capacity < max(0.05 * inc, 1000):
        triggers.append({"type": "LOW_SAVINGS", "label": "Low savings capacity", "icon": "savings"})

    return triggers


def get_aoai_client():
    from openai import AzureOpenAI

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    key = os.getenv("AZURE_OPENAI_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g. "retail-demo-gpt4omini"

    missing = [k for k, v in {
        "AZURE_OPENAI_ENDPOINT": endpoint,
        "AZURE_OPENAI_KEY": key,
        "AZURE_OPENAI_DEPLOYMENT": deployment
    }.items() if not v]

    if missing:
        raise ValueError(f"Missing env vars: {', '.join(missing)}")

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=key,
        api_version="2024-02-01"
    )
    return client, deployment



# LLM-based offer generation (the "glue")
# - Uses triggers (WHEN)
# - Uses model to craft offers (WHAT)
# - Uses stored memory to reference last interaction (LONG-TERM MEMORY)



SYSTEM_PROMPT = """You are a "Retail Bank Advisor - an intelligent, proactive and trustworthy Agentic AI Personal Banking Assistant for a Retail Bank.
Your personality: Warm, encouraging, professional, and customer-obsessed. You speak like a trusted financial advisor who truly knows their customer.

Rules:
- You will be provided with customer context + transaction summary + triggers + previous recommendations (this is your memory).
- You must generate EXACTLY 2 offers in JSON format (no extra text outside JSON).
- Offers must be relevant to the triggers and customer segment.
- Use Kenyan context: KSh, mobile money, common life goals.
- Be transparent in reasoning (include a short "reason" field per offer).


Return ONLY valid JSON with this structure:
{
  "advisor_message": "Short, friendly summary in 2-4 sentences.",
  "offers": [
    {
      "id": "offer_x",
      "type": "string",
      "title": "string",
      "body": "string",
      "cta": "string",
      "monthly_deposit": number,
      "icon": "string",
      "color": "string",
      "reason": "string"
    },
    {... second offer ...}
  ]
}
"""

def generate_offers_with_llm(customer, triggers):  # This function: takes a customer, takes detected triggers, generates AI-powered offers
    # load memory if exists
    mem = MEMORY.get(customer["customer_id"], {})
    previous_summary = mem.get("last_recommendation", "None (first interaction).")

    transactions = CUSTOMER_TRANSACTIONS[customer["customer_id"]]
    recent_transactions = transactions[-15:]

    user_payload = {
        "customer_profile": {
            "name": customer["name"],
            "segment": customer["segment"],
            "savings_goal": customer["savings_goal"]
        },
        "transaction_history": recent_transactions,
        "triggers": triggers,
        "previous_recommendation_summary": previous_summary
    }

    client, deployment = get_aoai_client()

    # IMPORTANT: In Azure OpenAI, `model` should be your DEPLOYMENT NAME
    resp = client.chat.completions.create(
            model=deployment,
            temperature=0.4,
            max_tokens=700,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(user_payload)}
            ]
        )

    text = resp.choices[0].message.content
    # Parse JSON safely
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        # Fallback: return safe default offers if model didn't return valid JSON
        result = {
            "advisor_message": "I generated tailored offers based on your recent activity, but the response format was not JSON. Showing safe fallback offers.",
            "offers": [
                {
                    "id": "fallback_1",
                    "type": "Goal-Based Savings",
                    "title": f"Boost your {customer.get('savings_goal','savings')}",
                    "body": "Start a goal-based plan with a comfortable monthly auto-save.",
                    "cta": "Start saving",
                    "monthly_deposit": 2000,
                    "icon": "rocket_launch",
                    "color": "green",
                    "reason": "Helps build consistent savings towards your goal."
                },
                {
                    "id": "fallback_2",
                    "type": "Round-up Savings",
                    "title": "Save automatically on every purchase",
                    "body": "Round up transactions and save the difference effortlessly.",
                    "cta": "Turn on round-ups",
                    "monthly_deposit": 1000,
                    "icon": "autorenew",
                    "color": "purple",
                    "reason": "Small automatic savings add up without effort."
                }
            ]
        }

    # Ensure 2 offers max
    offers = result.get("offers", [])[:2]
    for o in offers:
        o.setdefault("id", str(uuid.uuid4())[:8])

    # Save memory (glue!)
    MEMORY[customer["customer_id"]] = {
        "timestamp": now_str(),
        "last_recommendation": result.get("advisor_message", ""),
        "last_offers": offers
    }

    return result.get("advisor_message", ""), offers

# -----------------------------
# Health check: confirms model is callable
# -----------------------------
def health_check():
    try:
        client, deployment = get_aoai_client()
        resp = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": "Ping"}],
            max_tokens=10
        )
        return {"status": "ok", "deployment": deployment}
    except Exception as e:
        return {"status": "error", "error": str(e)}

# -----------------------------
# HTTP Handler
# -----------------------------
class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)

        # /health endpoint
        if parsed.path == "/health":
            payload = health_check()
            self._send_json(payload, status=200 if payload["status"] == "ok" else 500)
            return

        # Default endpoint: /?customer_id=C001
        params = parse_qs(parsed.query)
        customer_id = params.get("customer_id", ["C001"])[0]

        customer = CUSTOMERS.get(customer_id, CUSTOMERS["C001"])
        triggers = detect_triggers(customer)

        # Call the LLM to produce offers + advisor message
        try:
            advisor_message, offers = generate_offers_with_llm(customer, triggers)
            aoai_status = "connected"
        except Exception as e:
            advisor_message = "AI service not available. Showing fallback offers."
            offers = [
                {
                    "id": "fallback_1",
                    "type": "Round-up Savings",
                    "title": "Save automatically on every purchase",
                    "body": "Round up transactions and save the difference effortlessly.",
                    "cta": "Turn on round-ups",
                    "monthly_deposit": 1000,
                    "icon": "autorenew",
                    "color": "purple",
                    "reason": "Small automatic savings add up without effort."
                },
                {
                    "id": "fallback_2",
                    "type": "Goal-Based Savings",
                    "title": f"Start a goal plan for {customer.get('savings_goal','your goal')}",
                    "body": "Set a simple monthly auto-save to build consistency.",
                    "cta": "Start saving",
                    "monthly_deposit": 2000,
                    "icon": "rocket_launch",
                    "color": "green",
                    "reason": "A consistent plan helps you reach your goal faster."
                }
            ]
            aoai_status = f"error: {str(e)}"

        payload = {
            "aoai_status": aoai_status,
            "customer": customer,
            "triggers": triggers,
            "advisor_message": advisor_message,
            "offers": offers,
            "memory": MEMORY.get(customer["customer_id"], {}),
            "all_customers": [
                {"id": k, "name": v["name"], "segment": v["segment"], "avatar": v["avatar"]}
                for k, v in CUSTOMERS.items()
            ]
        }

        self._send_json(payload, status=200)

    def _send_json(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def log_message(self, format, *args):
        # silence default logging
        pass
