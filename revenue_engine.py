import pandas as pd

def analyze_menu(data_path):

    df = pd.read_csv(data_path)

    # Calculate profit margin
    df["margin"] = df["price"] - df["food_cost"]

    # Calculate average values
    avg_margin = df["margin"].mean()
    avg_sales = df["quantity"].mean()

    categories = []

    for i in range(len(df)):

        margin = df.loc[i, "margin"]
        sales = df.loc[i, "quantity"]

        if margin >= avg_margin and sales >= avg_sales:
            categories.append("Star")

        elif margin >= avg_margin and sales < avg_sales:
            categories.append("Puzzle")

        elif margin < avg_margin and sales >= avg_sales:
            categories.append("Plowhorse")

        else:
            categories.append("Dog")

    df["menu_category"] = categories

    return df