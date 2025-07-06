import pandas as pd

# Load the seasons from Filters.csv
df = pd.read_csv('data/Filters.csv')

print("=== ALL SEASONS ===")
print(f"Total seasons: {len(df)}")
print()

for _, row in df.iterrows():
    print(f"{row['FilterNumber']:2d}: {row['FilterName']}") 