import anthropic
from datetime import date
from dotenv import load_dotenv
from financer import FinanceAnalyzer, UserProfile
from tools import TOOLS, run_tool
from rag import StrategyStore


load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-5-5"

def build_system_prompt(user: UserProfile) -> str:
    return (
        f"You are a finance assistant for {user.name}. "
        f"Today's date is {date.today().isoformat()}. "
        f"Monthly income: ${user.monthly_income:.2f}, paid {user.pay_schedule}. "
        f"Budgets by category: {user.budgets}. "
        f"Savings goals: {user.savings_goals}. "
        "Always use the tools to get numbers, never calculate or guess amounts yourself. "
        "Months are in YYYY-MM format. "
        "If a tool returns an error, read it and try again with corrected input. "
        "When giving advice, use search_strategies and base suggestions on the strategies it returns, applied to the user's actual numbers. "
        "Keep answers short and clear."
    )

def ask(analyzer: FinanceAnalyzer, store: StrategyStore, question: str, messages: list) -> str:    
    messages.append({"role": "user", "content": question})
    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=build_system_prompt(analyzer.user),
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  [calling {block.name}({block.input})]")
                output = run_tool(analyzer, store, block.name, block.input)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
        messages.append({"role": "user", "content": results})

def main():

    user = UserProfile(    
        id=1,
        name="John Doe",
        monthly_income=2972.00,
        pay_schedule="weekly",
        accounts=[
            {"name": "checking", "type": "checking"},
            {"name": "college fund", "type": "savings"},
        ],
        budgets={
            "rent": 1100,
            "groceries": 300,
            "dining": 150,
            "gas": 120,
            "subscriptions": 50,
            "shopping": 150,
        },
        savings_goals=[
            {"name": "college fund", "target": 14000, "by": "2027-08-15"},
            {"name": "emergency fund", "target": 8000, "by": "2027-12-31"},
        ],

)
    store = StrategyStore("strategies.json")

    analyzer = FinanceAnalyzer(user)
    analyzer.load_transactions("transactions.csv")

    messages = []
    print("Finance agent ready. Type 'quit' to exit.")

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in {"quit", "exit"}:
            break
        if not question:
            continue
        print("\nAgent:", ask(analyzer, store, question, messages))



if __name__ == "__main__":
    main()