# voice_order_text.py
import pandas as pd
import json

# Load menu data
data = pd.read_csv("data/restaurant_data.csv")
data["margin"] = data["price"] - data["food_cost"]

# --- Parameters for AI logic ---
avg_margin = data["margin"].mean()
avg_quantity = data["quantity"].mean()

# --- Text Input for Order (instead of voice) ---
order_text = input("🍔 Type your order (e.g., Burger, Pizza, Fries): ")

# --- Match items in menu ---
ordered_items = []
for item in data['item']:
    if item.lower() in order_text.lower():
        ordered_items.append(item)

if not ordered_items:
    print("⚠️ No menu items recognized from your order.")
else:
    print("\n✅ Matched Items:", ordered_items)

# --- AI Upsell Suggestions ---
print("\n🔝 AI Upsell Suggestions:")
for item in ordered_items:
    row = data[data['item'] == item].iloc[0]
    if row["margin"] > avg_margin and row["quantity"] < avg_quantity:
        print(f"Promote {item} — high profit but low sales")
    elif row["margin"] < avg_margin and row["quantity"] > avg_quantity:
        print(f"Promote combo for {item} — low margin but high sales")
    else:
        print(f"{item} — price looks optimal")

# --- AI Price Optimization Suggestions ---
print("\n💰 Price Optimization Suggestions:")
for item in ordered_items:
    row = data[data['item'] == item].iloc[0]
    if row["margin"] < avg_margin and row["quantity"] > avg_quantity:
        print(f"Increase price of {item} slightly")
    elif row["margin"] > avg_margin and row["quantity"] < avg_quantity:
        print(f"Consider promoting {item} to increase sales")
    else:
        print(f"{item} — price looks optimal")

# --- Calculate Total Price ---
total_price = 0
for item in ordered_items:
    row = data[data['item'] == item].iloc[0]
    total_price += row['price']

print(f"\n💳 Total Price: ₹{total_price}")

# --- Export Order as JSON ---
order_details = [{"item": item, "price": int(data[data['item']==item]['price'])} for item in ordered_items]

with open("latest_order.json", "w") as f:
    json.dump(order_details, f, indent=2)

print("\n📄 Order saved to latest_order.json")