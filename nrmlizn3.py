import pandas as pd
from scipy.stats import percentileofscore

def calculate_percentile_score(raw_score, raw_scores):
    return (percentileofscore(raw_scores, raw_score) / 100) * 100

def linear_interpolation(x, x1, y1, x2, y2):
    return (((y2 - y1) / (x2 - x1)) * (x - x1)) + y1

# Load your Excel file into a pandas DataFrame
xl_file_path = "E:/sample data 2.xlsx"
df = pd.read_excel(xl_file_path)
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
    if index < len(df) - 1:
        x2 = df.at[index + 1, 'percentile_score']
        y2 = df.at[index + 1, 'raw_score'] 
    else:
        x2 = 0  # There is no next row
        y2 = 0

    # Get the previous row's 'percentile_score' and 'raw_score'
    if index > 0:
        x1 = df.at[index - 1, 'percentile_score']
        y1 = df.at[index - 1, 'raw_score'] 
    else:
        x1 = 0  # There is no previous row
        y1 = 0

    print(f"Index: {index}, x1: {x1}, x: {x}, x2: {x2}, y1: {y1}, y2: {y2}")

    normalization_score = linear_interpolation(x, x1, y1, x2, y2)
    df.at[index, 'normalization_score'] = normalization_score

print(df)
# Save the updated DataFrame to a new Excel file
output_file_path = 'output_scores02.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Percentile and normalization scores calculated and saved to {output_file_path}")
