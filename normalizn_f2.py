import os
import pandas as pd
import numpy as np

def calculate_percentile_score(raw_score, raw_scores):
    return (np.searchsorted(np.sort(raw_scores), raw_score, side='right') / len(raw_scores)) * 100

def linear_interpolation(x, x1, y1, x2, y2):
    return y1 + ((y2 - y1) / (x2 - x1)) * (x - x1)

def calculate_normalized_score(raw_scores, percentiles):
    normalized_scores = []

    for p in percentiles:
        raw_scores_p = raw_scores[percentiles == p]
        normalized_scores.append(raw_scores_p.mean())

    return np.array(normalized_scores)

def process_folder(folder_path):
    output_dfs = []

    # Read each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        df_shift = pd.read_csv(file_path)

        # Step 1: Calculate Percentiles
        df_shift['Percentile'] = df_shift['RawScore'].apply(
            lambda raw_score: calculate_percentile_score(raw_score, df_shift['RawScore']))

        # Step 2: Linear Interpolation
        df_shift['RawScore'] = df_shift['RawScore'].interpolate()

        # Step 3: Calculate Normalized Score
        normalized_scores = calculate_normalized_score(df_shift['RawScore'].values, df_shift['Percentile'].values)
        df_shift['NormalizedScore'] = normalized_scores

        output_dfs.append(df_shift)

    return output_dfs

# Replace 'folder_path' with the path to your folder containing shifts
folder_path = "E:/2023-2024/CSIR/Result/testNm/"
output_dfs = process_folder(folder_path)

# Save the updated DataFrames to new CSV files
for idx, df_shift in enumerate(output_dfs):
    output_file_path = f'output_shift_{idx + 1}_with_normalization.csv'
    df_shift.to_csv(output_file_path, index=False)
    print(f"Shift {idx + 1}: Percentile, linear interpolation, and normalized scores calculated and saved to {output_file_path}")
