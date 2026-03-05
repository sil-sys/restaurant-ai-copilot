# dashboard_text_order.py
import streamlit as st
import pandas as pd
import json

# --- Load Data ---
data = pd.read_csv("data/restaurant_data.csv")
data["margin"] = data["price"] - data["food_cost"]

avg_margin = data["margin"].mean()
avg_quantity = data["quantity"].mean()

# --- Sidebar: Adjustable Parameters ---
st.sidebar.header("⚙️ Adjust Parameters")
avg_margin_slider = st.sidebar.slider("Avg Margin Threshold", float(data['margin'].min()), float(data['margin'].max()), float(avg_margin))
avg_quantity_slider = st.sidebar.slider("Avg Quantity Threshold", float(data['quantity'].min()), float(data['quantity'].max()), float(avg_quantity))
min_support_slider = st.sidebar.slider("Min Support for Combos", 0.01, 1.0, 0.05, 0.01)

# --- Main Dashboard ---
st.title("🍽️ AI Restaurant Analytics Dashboard")

# --- Menu Profitability Analysis ---
st.subheader("📊 Menu Profitability Analysis")
st.dataframe(data[['item', 'price', 'food_cost', 'margin', 'quantity']])

# --- Text Order Input ---
st.subheader("📝 Type Customer Order")
order_text = st.text_input("Enter items separated by comma (e.g., Burger, Pizza, Fries):")

ordered_items = []
if order_text:
    for item in data['item']:
        if item.lower() in order_text.lower():
            ordered_items.append(item)
    if not ordered_items:
        st.warning("⚠️ No menu items recognized from your order.")
    else:
        st.success(f"✅ Matched Items: {', '.join(ordered_items)}")

# --- AI Upsell Suggestions ---
if ordered_items:
    st.subheader("🔝 AI Upsell Suggestions")
    for item in ordered_items:
        row = data[data['item'] == item].iloc[0]
        if row["margin"] > avg_margin_slider and row["quantity"] < avg_quantity_slider:
            st.write(f"Promote {item} — high profit but low sales")
        elif row["margin"] < avg_margin_slider and row["quantity"] > avg_quantity_slider:
            st.write(f"Promote combo for {item} — low margin but high sales")
        else:
            st.write(f"{item} — price looks optimal")

# --- AI Price Optimization Suggestions ---
if ordered_items:
    st.subheader("💰 AI Price Optimization Suggestions")
    for item in ordered_items:
        row = data[data['item'] == item].iloc[0]
        if row["margin"] < avg_margin_slider and row["quantity"] > avg_quantity_slider:
            st.write(f"Increase price of {item} slightly")
        elif row["margin"] > avg_margin_slider and row["quantity"] < avg_quantity_slider:
            st.write(f"Consider promoting {item} to increase sales")
        else:
            st.write(f"{item} — price looks optimal")

# --- Total Price ---
if ordered_items:
    total_price = sum([data[data['item']==item]['price'].iloc[0] for item in ordered_items])
    st.subheader("💳 Total Price")
    st.write(f"₹{total_price}")

    # --- Export Order as JSON ---
    order_details = [{"item": item, "price": int(data[data['item']==item]['price'])} for item in ordered_items]
    with open("latest_order.json", "w") as f:
        json.dump(order_details, f, indent=2)
    st.write("📄 Order saved to latest_order.json")