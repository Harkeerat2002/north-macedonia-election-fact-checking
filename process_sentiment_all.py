import os
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Folder containing the CSVs
FOLDER = "PreprocessedDataset"

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Check CSV columns before processing
files = [f for f in os.listdir(FOLDER) if f.endswith(".csv")]
for f in files:
    path = os.path.join(FOLDER, f)
    df = pd.read_csv(path)
    print(f"\n--- {f} ---")
    print(df.columns.tolist())

# Function to compute sentiment
def add_sentiment(df):
    sentiments = df['caption'].astype(str).apply(analyzer.polarity_scores).tolist()
    sentiment_df = pd.DataFrame(sentiments)
    df = pd.concat([df, sentiment_df], axis=1)
    df['sentiment_label'] = df['compound'].apply(
        lambda x: 'positive' if x >= 0.05 else 'negative' if x <= -0.05 else 'neutral'
    )
    return df

# Process each CSV
processed_dfs = []

for file in os.listdir(FOLDER):
    if file.endswith(".csv"):
        path = os.path.join(FOLDER, file)
        df = pd.read_csv(path)

        # Find text column (caption or claims)
        text_col = next((col for col in df.columns if col.strip().lower() in ['caption', 'claims']), None)

        if text_col:
            print(f"Processing: {file} using column '{text_col}'")
            df['caption'] = df[text_col].astype(str)  # unify column name
            df = add_sentiment(df)
            df['source_file'] = file
            df['party'] = file.split('_')[0]  # derive party name from filename
            processed_dfs.append(df)
        else:
            print(f"Skipped (no 'caption' or 'claims' column): {file}")

# Combine all processed data
if processed_dfs:
    combined_df = pd.concat(processed_dfs, ignore_index=True)
    combined_df.to_csv("sentiment_combined.csv", index=False)
    print("✅ Saved combined sentiment results to 'sentiment_combined.csv'")
else:
    print("❌ No datasets with a usable text column ('caption' or 'claims') were found.")

# Final check
df = pd.read_csv("sentiment_combined.csv")
print("\n📄 Final columns:")
print(df.columns)
print("\n📁 Files processed:")
print(df[['source_file']].drop_duplicates())
print("\n🧭 Parties:")
print(df['party'].unique())
