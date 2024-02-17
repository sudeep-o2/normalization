import pandas as pd
from scipy.stats import percentileofscore

def calculate_percentile_score(raw_score, raw_scores):
    return (percentileofscore(raw_scores, raw_score) / 100) * 100

def linear_interpolation(x, x1, y1, x2, y2):
    return (((y2 - y1) / (x2 - x1)) * (x - x1)) + y1

# Load your Excel file into a pandas DataFrame
csv_file_path = "E:/normalization.csv"
df = pd.read_csv(csv_file_path)
print(df)

# Calculate percentile score for each row
for index, row in df.iterrows():
    raw_score = row['raw_score']  # Replace 'raw_score' with the actual column name containing raw scores
    raw_scores = df['raw_score']  # Replace 'raw_score' with the actual column name containing raw scores

    percentile_score = calculate_percentile_score(raw_score, raw_scores)
    df.at[index, 'percentile_score'] = percentile_score

# Sort DataFrame by 'percentile_score' for linear interpolation
df = df.sort_values(by='percentile_score')

print(df)

# Perform linear interpolation for normalization score
for index, row in df.iterrows():
    x = row['percentile_score']
    x1 = df['percentile_score'].shift(-1).iloc[index]
    x2 = df['percentile_score'].shift(1).iloc[index]
    y1 = df['raw_score'].shift(-1).iloc[index]
    y2 = df['raw_score'].shift(1).iloc[index]

    print(f"Index: {index}, x1: {x1}, x: {x}, x2: {x2}, y1: {y1}, y2: {y2}")

    normalization_score = linear_interpolation(x, x1, y1, x2, y2)
    df.at[index, 'normalization_score'] = normalization_score

print(df)
# Save the updated DataFrame to a new Excel file
output_file_path = 'output_scores.csv'
df.to_csv(output_file_path, index=False)

print(f"Percentile and normalization scores calculated and saved to {output_file_path}")
