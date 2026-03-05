import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Load your restaurant sales data
data = pd.read_csv("data/restaurant_data.csv")

# Convert transactional data to a basket format
basket = data.groupby(['order_id', 'item'])['quantity'].sum().unstack().fillna(0)
basket = basket.applymap(lambda x: 1 if x > 0 else 0)

# Run Apriori to find frequent itemsets
frequent_itemsets = apriori(basket, min_support=0.05, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)

# Sort rules by confidence
rules = rules.sort_values('confidence', ascending=False)

print("\nAI Combo Recommendations:\n")
for _, row in rules.head(10).iterrows():
    items = ', '.join(list(row['antecedents'])) + " → " + ', '.join(list(row['consequents']))
    print(f"Consider combo: {items} (Confidence: {row['confidence']:.2f})")