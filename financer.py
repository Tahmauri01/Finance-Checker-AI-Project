import csv
from dataclasses import dataclass

@dataclass
class Transaction:
    # Transactions of csv file and it's attributes

    id: int
    date: str
    name: str
    amount: float
    account: str
    category: str
    type: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "Transaction":
        return cls(
            id=int(row["id"]),
            date=row["date"],
            name=row["name"],
            account=float(row["account"]),
            category=row["category"],
            type=row["type"],
        )

@dataclass
class 

