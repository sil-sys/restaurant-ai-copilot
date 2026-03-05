import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Restaurant AI Revenue Intelligence Dashboard")

data = pd.read_csv("data/restaurant_data.csv")

# Calculate margin
data["margin"] = data["price"] - data["food_cost"]

# Average values
avg_margin = data["margin"].mean()
avg_quantity = data["quantity"].mean()

# Menu engineering classification
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

st.subheader("Menu Data")
st.dataframe(data)

# Category distribution chart
category_counts = data["menu_category"].value_counts().reset_index()
category_counts.columns = ["Category", "Count"]

fig = px.bar(category_counts, x="Category", y="Count",
             title="Menu Engineering Distribution")

st.plotly_chart(fig)

# AI insights
st.subheader("AI Insights")

st.write("⭐ Star Items (High margin + high sales)")
st.dataframe(data[data["menu_category"] == "Star"])

st.write("🧩 Puzzle Items (High margin but low sales)")
st.dataframe(data[data["menu_category"] == "Puzzle"])

st.write("🐎 Plowhorse Items (Low margin but high sales)")
st.dataframe(data[data["menu_category"] == "Plowhorse"])

st.write("🐶 Dog Items (Low margin + low sales)")
st.dataframe(data[data["menu_category"] == "Dog"])