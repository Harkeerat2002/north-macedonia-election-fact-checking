import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv('DUI.csv')

# Visualization 1: Visualize all column names
plt.figure(figsize=(10, 6))
plt.bar(df.columns, [1] * len(df.columns), color='skyblue')
plt.title("Column Names in the CSV")
plt.xlabel("Column Names")
plt.ylabel("Placeholder Value")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Visualization 2: Visualize the first 3-4 rows
plt.figure(figsize=(10, 6))
plt.axis('off')  # Turn off the axes
plt.table(cellText=df.head(4).values, colLabels=df.columns, loc='center', cellLoc='center')
plt.title("First 3-4 Rows of the CSV")
plt.show()