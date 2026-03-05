from revenue_engine import analyze_menu

data_path = "data/restaurant_data.csv"

df = analyze_menu(data_path)

print("\nMenu Engineering Analysis:\n")
print(df[["item","margin","quantity","menu_category"]])