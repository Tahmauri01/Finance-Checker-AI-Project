import json
from dataclasses import asdict, is_dataclass
from rag import StrategyStore

TOOLS = [
{
    "name": "spending_by_category",
    "description": (
        "Calculates total amount spent in each category of a specific month. "
        "Returns each category's total for the month specified. "
        "Use this for questions asking for how much was spent on a certain category in a month. Ex: 'How much did I spend on gas in September?' "
        "Amounts are positive dollar values. Only expenses are counted. "
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "month": {
                "type": "string",
                "description": "The month in a YYYY-MM format. EX: 2026-10"
            },
        },
        "required": ["month"]
    }
},
{
    "name": "compare_months",
    "description": (
        "Compares transactions grouped by category between two months. "
        "Returns each month's category total side by side. "
        "Use this for questions comparing two months. Ex: 'Did I spend more money in March or February?'. "
        "Amounts are positive dollar values. Only expenses are counted. "
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "month_a":{
                "type": "string",
                "description": "The first month, being compared to month_b. Entered in a YYYY-MM format. Should not match month_b"
            },
            "month_b":{
                "type": "string",
                "description": "The second month, being compared to month_a. Entered in a YYYY-MM format. Should not match month_a"
            }
        },
        "required": ["month_a", "month_b"]
    }
},
{
    "name": "monthly_total",
    "description": (
        "Calculates each month's total expenses based on the specified year. "
        "Returns the total of the expenses for every month in that specific year. "
        "Use for questions asking how much was spent in a certain month. Ex: 'How much did I spend in January 2024?' "
        "Amounts are positive dollar values. Only expenses are counted. "
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "year": {
                "type": "integer",
                "description": "The year of which months will be calculated. Entered in YYYY format."
            }
        },
        "required": ["year"],
    }
},
{
    "name": "least_spending_month",
    "description": (
        "Determines the month with the lowest expense for the specified year. "
        "Returns the month with the smallest total expenses for the year specified. "
        "Use for questions asking which month they spent the least money in. Ex: 'In 2021, which month did I spend the least in?' "
        "Amounts are positive dollar values. Only expenses are counted. "
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "year": {
                "type": "integer",
                "description": "The year of which month's expenses will be compared. Entered in YYYY format."
            }
        },
        "required": ["year"],
    }
},
{
    "name": "highest_spending_month",
    "description": (
        "Determines the month with the highest expense for the specified year. "
        "Returns the month with the largest total expenses for the year specified. "
        "Use for questions asking which month they spent the most money in. Ex: 'In 2021, which month did I spend the most in?' "
        "Amounts are positive dollar values. Only expenses are counted. "
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "year": {
                "type": "integer",
                "description": "The year of which month's expenses will be compared. Entered in YYYY format."
            }
        },
        "required": ["year"],
    }
},
{
    "name": "largest_seen",
    "description": (
        "Determines the top n largest expenses in entire financial file. "
        "Returns top n largest expenses in financial file listed from largest to smallest. "
        "Use for questions asking what the largest expenses are. Ex: 'What are my top 10 largest expenses?' "
        "Amounts are positive dollar values. Only expenses are counted. "
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "n": {
                "type": "integer",
                "decription": "The amount of transactions listed"
            }
        },
        "required": [],
    }
},
{
    "name": "recurring_charges",
    "description": (
        "Determines transactions from the same merchant that occur more than once. "
        "Returns list of the merchant names that repeat. "
        "Use for questions asking what their subscriptions or reoccuring charges are. Ex: What subcriptions am I signed up for?"
    ),
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
    }
},
{
    "name": "find_uncategorized",
    "description": (
        "Determines all transactions with a category of None. "
        "Returns lists of transactions with a category of None. "
        "Use to find transactions with no categories to then combine it with the categorize method"
    ),
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
    }
},
{
    "name": "categorize",
    "description": (
        "Applies an existing category to a transaction. "
        "Returns the count of transactions that had their categories changes. "
        "Use when asked to categorize a transaction. Ex: If there is a transaction without a category, change it to groceries."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "transaction_ids": {
                "type": "array",
                "description": "List of transaction ids whose transaction categories is being changed."
            },
            "category": {
                "type": "string",
                "description": "Category of which the transaction is being changed to."
            }
        },
        "required": ["transaction_ids", "category"]
    }
},
{
    "name": "search_strategies",
    "description": (
        "Search a library of saving and budgeting strategies. "
        "Use when the user asks for advice, is over budget, is behind on a savings goal, "
        "or would benefit from a strategy. Describe their situation in the query. "
        "Returns the most relevant strategies with a similarity score."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The user's situation in plain words, e.g. 'overspending on dining, behind on emergency fund'.",
            },
            "k": {
                "type": "integer",
                "description": "How many strategies to return. Defaults to 3.",
            },
        },
        "required": ["query"],
    },
},
]

def to_text(result) -> str:
    if isinstance(result, list):
        result = [asdict(r) if is_dataclass(r) else r for r in result]
    return json.dumps(result, default=str)

def run_tool(analyzer, store, name: str, args: dict) -> str:
    methods = {
        "spending_by_category": analyzer.spending_by_category,
        "compare_months": analyzer.compare_months,
        "monthly_total": analyzer.monthly_total,
        "least_spending_month": analyzer.least_spending_month,
        "highest_spending_month": analyzer.highest_spending_month,
        "largest_seen": analyzer.largest_seen,
        "recurring_charges": analyzer.recurring_charges,
        "find_uncategorized": analyzer.find_uncategorized,
        "categorize": analyzer.categorize,
        "search_strategies": store.search_strategies,
    }

    if name not in methods:
        return f"Error: unknown tool: {name}"
    try:
        return to_text(methods[name](**args))
    except Exception as e:
        return f"Error: {e}"    