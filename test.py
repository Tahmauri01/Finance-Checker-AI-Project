from financer import Transaction, UserProfile, FinanceAnalyzer

user = UserProfile(
    id=1,
    name="John Doe",
    monthly_income=2972.00,
    pay_schedule="weekly",
    accounts= [
        {"name": "checking", "type": "checking"},
        {"name": "college fund", "type": "saving"}
    ],
    budgets= {
        "groceries": 200,
        "bills": 800
    },
    savings_goals= [
        {"name": "college fund", "target": 14000, "by": "2026-11-02"},
        {"name": "emergency funds", "target": 8000, "by": "2026-12-20"}
    ]
)

analyzer = FinanceAnalyzer(user)
analyzer.load_transactions("transactions.csv")

# Money spent per month
print(analyzer.monthly_total(2026))

# money spent in each category
print(analyzer.spending_by_category("2026-10"))

# ---- compare_months ----
print("\ncompare_months('2026-03', '2026-04'):")
print(analyzer.compare_months("2026-03", "2026-04"))

# ---- least / highest spending month ----
print("\n" + analyzer.least_spending_month(2026))
print(analyzer.highest_spending_month(2026))

# ---- largest_seen ----
print("\nTop 5 largest expenses:")
for t in analyzer.largest_seen():
    print(f"  {t.date} {t.description}: {t.amount}")

largest = analyzer.largest_seen(3)
assert len(largest) == 3
assert abs(largest[0].amount) >= abs(largest[1].amount) >= abs(largest[2].amount)
assert all(t.type == "expense" for t in largest)

# ---- recuring_charges ----
recurring = analyzer.recuring_charges()
print(f"\nRecurring charges ({len(recurring)}):")
print(recurring)
assert "Rent" in recurring
assert "Meal Kit Subscription" in recurring
assert "Streaming Service" in recurring

# ---- find_uncategorized ----
uncategorized = analyzer.find_uncategorized()
print(f"\nUncategorized transactions: {len(uncategorized)}")
for t in uncategorized[:5]:
    print(f"  {t.id} {t.date} {t.description} ({t.type})")
assert all(t.category is None for t in uncategorized)

# ---- categorize ----
# grab two uncategorized *expenses* and categorize them as "other"
expense_ids = [t.id for t in uncategorized if t.type == "expense"][:2]
count = analyzer.categorize(expense_ids, "other")
print(f"\nCategorized {count} transactions as 'other'")
assert count == len(expense_ids)
assert len(analyzer.find_uncategorized()) == len(uncategorized) - count

# invalid category should raise ValueError
try:
    analyzer.categorize(expense_ids, "not-a-category")
    print("ERROR: invalid category was accepted")
except ValueError as e:
    print(f"Invalid category correctly rejected: {e}")

print("\nAll tests passed")

# ================= edge-case / breaking tests =================
print("\n--- Edge case tests (designed to expose bugs) ---")

def check(description, condition):
    print(f"{'PASS' if condition else 'FAIL'}: {description}")

# 1. spending_by_category with a nonsense month string — no validation exists
check("invalid month string returns empty dict", analyzer.spending_by_category("banana") == {})

# 2. valid month with no data
check("month with no data returns empty dict", analyzer.spending_by_category("2024-01") == {})

# 3. least_spending_month for a year with NO transactions
#    monthly_total fills all 12 months with 0, so totals is never empty and
#    the "No spending data" branch can never run
result = analyzer.least_spending_month(2024)
check("empty year reports 'No spending data'", result == "No spending data for 2024")
print(f"    actual: {result}")

# 4. largest_seen with n=0 and negative n
check("largest_seen(0) returns empty list", analyzer.largest_seen(0) == [])
neg = analyzer.largest_seen(-1)
check("largest_seen(-1) returns nothing (not almost-everything)", len(neg) <= 1)
print(f"    largest_seen(-1) returned {len(neg)} transactions")

# 5. categorize with ids that don't exist — succeeds silently with count 0
check("categorize with unknown ids returns 0", analyzer.categorize([99999], "dining") == 0)

# 6. categorize happily relabels an INCOME transaction
income_ids = [t.id for t in analyzer.transactions if t.type == "income"][:1]
count = analyzer.categorize(income_ids, "shopping")
check("categorize refuses income transactions", count == 0)
print(f"    actually categorized {count} income transaction(s) as 'shopping'")

# 7. compare_months with the same month twice — dict keys collide
result = analyzer.compare_months("2026-05", "2026-05")
check("compare_months('2026-05','2026-05') returns 2 entries", len(result) == 2)

# 8. loading a file that doesn't exist
try:
    FinanceAnalyzer(user).load_transactions("does_not_exist.csv")
    print("FAIL: missing csv did not raise an error")
except FileNotFoundError:
    print("PASS: missing csv raises FileNotFoundError")

# 9. malformed row — non-numeric amount crashes from_row with a raw ValueError
import csv, os
bad_path = "bad_transactions.csv"
with open(bad_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "date", "description", "amount", "account", "category", "type"])
    w.writerow([1, "2026-01-01", "Broken Row", "twelve dollars", "Checking", "dining", "expense"])
try:
    FinanceAnalyzer(user).load_transactions(bad_path)
    print("FAIL: malformed amount was accepted")
except ValueError as e:
    print(f"NOTE: malformed amount raises raw ValueError: {e}")
finally:
    os.remove(bad_path)
