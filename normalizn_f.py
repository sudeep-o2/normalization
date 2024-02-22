import os
import pandas as pd
from scipy.stats import percentileofscore

def calculate_percentile_score(raw_score, raw_scores):
    return (percentileofscore(raw_scores, raw_score) / 100) * 100

def linear_interpolation(x, x1, y1, x2, y2):
    if x1 == x2:
        return y1  # Return the same value for all rows with the same percentile score
    else:
        return (((y2 - y1) / (x2 - x1)) * (x - x1)) + y1

def calculate_normalized_marks(x, x1, y1, x2, y2):
    if x >= x1:
        return linear_interpolation(x, x1, y1, x2, y2)
    else:
        return y1 - (((y2 - y1) / (x2 - x1)) * (x1 - x))

def identify_base_shift(folder_path):
    base_shift_info = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        df_shift = pd.read_csv(file_path)

        mean_score = df_shift['raw_score'].mean()
        max_score = df_shift['raw_score'].max()
        candidate_count = df_shift.shape[0]

        base_shift_info.append({'shift': file_name, 'mean': mean_score, 'max': max_score, 'count': candidate_count})

    base_shift_df = pd.DataFrame(base_shift_info)
    base_shift_df = base_shift_df[base_shift_df['count'] >= 0.7 * base_shift_df['count'].mean()]
    base_shift_df = base_shift_df.sort_values(by=['mean', 'max', 'count'], ascending=[False, False, False]).iloc[0]

    return base_shift_df['shift']

def process_folder(folder_path, base_shift):
    output_dfs = []

    # Load the Base Shift DataFrame
    base_shift_path = os.path.join(folder_path, base_shift)
    base_shift_df = pd.read_csv(base_shift_path)

    for file_name in os.listdir(folder_path):
        if file_name == base_shift:
            # Skip processing the Base Shift file itself
            continue

        file_path = os.path.join(folder_path, file_name)
        df_shift = pd.read_csv(file_path)

        # Calculate percentile score for each row in the shift
        for index, row in df_shift.iterrows():
            raw_score = row['raw_score']  # Replace with the actual column name containing raw scores
            raw_scores = df_shift['raw_score']  # Replace with the actual column name containing raw scores

            percentile_score = calculate_percentile_score(raw_score, raw_scores)
            df_shift.at[index, 'percentile_score'] = percentile_score

        # Perform linear interpolation for normalization score
        for index, row in df_shift.iterrows():
            x = row['percentile_score']

            # Get the corresponding rows in the Base Shift DataFrame for linear interpolation
            base_shift_rows_filtered = base_shift_df[
                (base_shift_df['percentile_score'] <= x)
            ].sort_values(by='percentile_score').tail(2)

            if len(base_shift_rows_filtered) == 2:
                x1, y1 = base_shift_rows_filtered.iloc[0][['percentile_score', 'raw_score']]
                x2, y2 = base_shift_rows_filtered.iloc[1][['percentile_score', 'raw_score']]
                normalization_score = calculate_normalized_marks(x, x1, y1, x2, y2)
            else:
                # Handle the case where there is only one row in the Base Shift DataFrame
                normalization_score = base_shift_rows_filtered.iloc[0]['raw_score']

            df_shift.at[index, 'normalization_score'] = normalization_score

        output_dfs.append(df_shift)

    return output_dfs


# Replace 'folder_path' with the path to your folder containing shifts
folder_path = "E:/2023-2024/CSIR/Result/testNm"
base_shift = identify_base_shift(folder_path)
print(f"Base Shift identified: {base_shift}")

# Process each shift and calculate normalized marks
output_dfs = process_folder(folder_path, base_shift)

# Save the updated DataFrames to new CSV files
for idx, df_shift in enumerate(output_dfs):
    output_file_path = f'output_scores_shift_{idx + 1}_with_normalization.csv'
    df_shift.to_csv(output_file_path, index=False)
    print(f"Shift {idx + 1}: Percentile and normalization scores calculated and saved to {output_file_path}")
