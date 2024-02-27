import os
import pandas as pd
import numpy as np

def calculate_percentile_score(raw_score, raw_scores):
    sorted_scores = np.sort(raw_scores)
    percentile = (np.searchsorted(sorted_scores, raw_score, side='right') / len(sorted_scores)) * 100
    return percentile

def linear_interpolation(x, x1, y1, x2, y2):
    if x1 == x2:
        return y1  # Return the same value for all rows with the same percentile score
    else:
        return (((y2 - y1) / (x2 - x1)) * (x - x1)) + y1

def calculate_normalized_score(row, sessions):
    raw_scores = [row[f'RawScoreS{i}'] for i in range(1, sessions + 1) if not pd.isnull(row[f'RawScoreS{i}'])]
    return np.mean(raw_scores)

def process_folder(input_folder, sessions):
    output_dfs = []

    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        df_shift = pd.read_csv(file_path)

        # Calculate percentile score for each row in the shift
        df_shift['Percentile'] = df_shift['RawScore'].apply(lambda x: calculate_percentile_score(x, df_shift['RawScore']))

        # Perform linear interpolation for blank entries
        df_shift = df_shift.sort_values(by='Percentile', ascending=False)
        df_shift['RawScore'] = df_shift['RawScore'].interpolate()

        # Calculate normalized score
        df_shift['NormalizedScore'] = df_shift.apply(lambda row: calculate_normalized_score(row, sessions), axis=1)

        output_dfs.append(df_shift)

    return output_dfs

# Replace 'input_folder' with the path to your folder containing shifts
input_folder = "E:/2023-2024/CSIR/Result/testNm/"
sessions = 4  # Update this based on the number of sessions

# Process each shift and calculate percentile, linear interpolation, and normalized score
output_dfs = process_folder(input_folder, sessions)

# Save the updated DataFrames to new CSV files
for idx, df_shift in enumerate(output_dfs):
    output_file_path = f'output_shift2_{idx + 1}_with_normalization.csv'
    df_shift.to_csv(output_file_path, index=False)
    print(f"Shift {idx + 1}: Percentile, linear interpolation, and normalized scores calculated and saved to {output_file_path}")
