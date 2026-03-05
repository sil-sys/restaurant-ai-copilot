import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Example order dataset
orders = [
    ["Burger", "Fries"],
    ["Burger", "Coke"],
    ["Pizza", "Coke"],
    ["Burger", "Fries", "Coke"],
    ["Pizza", "Garlic Bread"],
    ["Burger", "Fries"]
]

# Convert to dataframe
df = pd.DataFrame(orders)

# One-hot encode
basket = pd.get_dummies(df.stack()).groupby(level=0).sum()

# Frequent itemsets
frequent = apriori(basket, min_support=0.3, use_colnames=True)

# Generate rules
rules = association_rules(frequent, metric="lift", min_threshold=1)

print(rules[["antecedents", "consequents", "support", "confidence"]])