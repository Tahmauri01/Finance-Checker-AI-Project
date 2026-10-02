import csv
from dataclasses import dataclass
from datetime import date

CATEGORIES = {"dining", "groceries", "gas", "rent", "subscriptions", "shopping", "other"}

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
        """Loads transactions from a csv file"""
        transactions = []

        with open(csv_path, 'r', newline='') as t_file:      #opens and reads csv file
            t_file_d = csv.DictReader(t_file)
            for row in t_file_d:
                transactions.append(Transaction.from_row(row))          #calls from_row to turn csv line into a transaction

            return transactions

    def spending_by_category(self, month: str) -> dict[str, float]:
        """Finds amount spent on each category in a given month"""
        totals = {}

        for t in self.transactions:
            if t.date.strftime("%Y-%m") == month:
                if t.type != "expense":
                    continue
                category = t.category or "uncategorized"
                totals[category] = totals.get(category, 0) + abs(t.amount)

        return totals


    def compare_months(self, month_a: str, month_b: str) -> dict[str, dict[str, float]]:
        return {
            month_a: self.spending_by_category(month_a),
            month_b: self.spending_by_category(month_b)
        }


    def monthly_total(self, year: int) -> dict[int, float]:             # helper function for least and highest spending month functions
        totals = {}
        for month in range(1,13):
            spent = sum(self.spending_by_category(f"{year}-{month:02d}").values())
            totals[month] = spent

        return totals

    def least_spending_month(self, year: int) -> str:
        totals = self.monthly_total(year)
        if not totals:
            return f"No spending data for {year}"

        month = min(totals, key=totals.get)
        amount = totals[month]
        name = date(year, month, 1).strftime("%B")

        return f"Least Spending Month: {name} - ${amount:.2f}"


    def highest_spending_month(self, year: int) -> str:
        """Finds month with the highest spending for given year"""
        totals = self.monthly_total(year)
        if not totals:
            return f"No spending data for {year}"

        month = max(totals, key=totals.get)
        amount = totals[month]
        name = date(year, month, 1).strftime("%B")

        return f"Highest Spending Month: {name} - ${amount:.2f}"

    
    def largest_seen(self, n: int = 5) -> list[Transaction]:
        """Finds top n largest expenses"""
        seen = []

        for t in self.transactions:
            if t.type == "expense":
                seen.append(t)

        return sorted(seen, key=lambda t: abs(t.amount), reverse=True)[:n]


    def recuring_charges(self) -> list[str]:
        """Finds recuring charges"""
        seen = set()
        repeat = set()

        for t in self.transactions:
            if t.type != "expense":
                continue
            if t.description not in seen:
                seen.add(t.description)
                continue
            repeat.add(t.description)

        return list(repeat)


    def find_uncategorized(self) -> list[Transaction]:
        """finds transactions without a category"""
        uncategorized = []

        for t in self.transactions:
            if t.category is None:
                uncategorized.append(t)

        return uncategorized

    def categorize(self, transaction_ids: list[int], category: str) -> int:

        if category not in CATEGORIES:
            raise ValueError(f"Use one of these categories: {CATEGORIES}")
        
        count = 0
        for t in self.transactions:
            if t.id in transaction_ids:
                t.category = category
                count += 1

        return count


    

