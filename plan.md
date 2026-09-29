Main Object:

Transaction(class):
Attributes - id, date, description, amount, account, category, type
Methods - from_row()

UserProfile(class):
Attributes - id, name, monthly_income, pay_schedule, accounts, budgets, savings_goals
Methods - N/A

FinanceAnalyzer(class):
Attributes - transactions
Methods - load_transactions(), compare_months(), spending_by_category(), least_spending_month(), highest_spending_month(), largest_expenses(), reoccuring_chargest(), categorize()