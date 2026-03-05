import pandas as pd

data = pd.read_csv("data/restaurant_data.csv")

data["margin"] = data["price"] - data["food_cost"]

avg_margin = data["margin"].mean()
avg_quantity = data["quantity"].mean()

def classify(row):
    if row["margin"] >= avg_margin and row["quantity"] >= avg_quantity:
        return "Star"
    elif row["margin"] >= avg_margin and row["quantity"] < avg_quantity:
        return "Puzzle"
    elif row["margin"] < avg_margin and row["quantity"] >= avg_quantity:
        return "Plowhorse"
    else:
        return "Dog"

data["menu_category"] = data.apply(classify, axis=1)

print("Upsell Recommendations:\n")

upsell_items = data[data["menu_category"] == "Puzzle"]

for item in upsell_items["item"]:
    print(f"Promote {item} more — high margin but low sales")