import csv
from dataclasses import dataclass
from datetime import date

@dataclass
class Transaction:
    # Transactions of csv file and it's attributes

    id: int
    date: date
    description: str
    amount: float
    account: str
    category: str | None
    type: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "Transaction":        #converts csv line into transaction
        return cls(
            id=int(row["id"]),
            date=date.fromisoformat(row["date"]),
            description=row["description"],
            amount=float(row["amount"]),
            account=row["account"],
            category=row["category"],
            type=row["type"],
        )

@dataclass
class UserProfile:         #creates user profile
    id: int
    description: str
    monthly_income: float
    pay_schedule: str
    accounts: list
    budgets: dict
    savings_goals: list


class FinanceAnalyzer:
    def __init__(self, user):
        self.user = user
        self.transactions: list[Transaction] = []

    @staticmethod
    def load_transactions(csv_path: str) -> list[Transaction]:
        transactions = []

        with open(csv_path, 'r', newline='') as t_file:      #opens and reads csv file
            t_file_d = csv.DictReader(t_file)
            for row in t_file_d:
                transactions.append(Transaction.from_row(row))          #calls from_row to turn csv line into a transaction

            return transactions


    def compare_months(self, month_a: str, month_b: str) -> dict[str, dict[str, float]]:
        pass

    def spending_by_category(self, month: str) -> dict[str, float]:
        totals = {}

        for t in self.transactions:
            if t.date.strftime("%Y-%m") == month:
                if t.type != "expense":
                    continue
                category = t.category or "uncategorized"
                totals[category] = totals.get(category, 0) + abs(t.amount)

        return totals

    def least_spending_month(self, year: int) -> str:
        pass

    def highest_spending_month(self, year: int) -> str:
        pass

    def largest_expenses(self, n: int = 5) -> list[Transaction]:
        pass

    def reccuring_charges(self) -> list[Transaction]:
        pass

    def get_uncategorized(self) -> list[Transaction]:
        pass

    def categorize(self, transaction_ids: list[int], category: str) -> int:
        pass


    

