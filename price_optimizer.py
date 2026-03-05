import pandas as pd

data = pd.read_csv("data/restaurant_data.csv")

data["margin"] = data["price"] - data["food_cost"]

avg_margin = data["margin"].mean()
avg_quantity = data["quantity"].mean()

def price_suggestion(row):
    if row["margin"] < avg_margin and row["quantity"] > avg_quantity:
        return f"Consider increasing price of {row['item']} slightly"
    elif row["margin"] > avg_margin and row["quantity"] < avg_quantity:
        return f"Consider promoting {row['item']} to increase sales"
    else:
        return "Price looks optimal"

data["price_recommendation"] = data.apply(price_suggestion, axis=1)

print("\nAI Price Optimization Suggestions:\n")

for rec in data["price_recommendation"]:
    print(rec)