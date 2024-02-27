"""import pandas as pd

# Assuming you have a list of file paths
file_paths = ["file1.csv", "file2.csv", "file3.csv"]

# Initialize an empty DataFrame to store the combined results
combined_df = pd.DataFrame()

# Iterate through each file
for i, file_path in enumerate(file_paths):
    # Read the file into a DataFrame
    df = pd.read_csv(file_path)

    # Merge the current DataFrame with the combined DataFrame on the 'Percentile' column
    if combined_df.empty:
        combined_df = df
    else:
        combined_df = pd.merge(combined_df, df, on='Percentile', how='outer', suffixes=('', f'_{i+1}'))

# Rename columns to RawScore1, RawScore2, ...
combined_df.columns = [col if 'RawScore' in col else f'RawScore{i+1}' for i, col in enumerate(combined_df.columns)]

# If you want to sort the DataFrame based on Percentile
combined_df = combined_df.sort_values(by='Percentile')

# Save the result to a new CSV file or do further processing as needed
combined_df.to_csv("combined_result.csv", index=False)"""


#round of required else may be correct 

import os
import pandas as pd
from scipy.stats import percentileofscore

def calculate_percentile_score(raw_score, raw_scores):

    N = len(raw_scores)
    
    # m is the count of candidates with raw scores less than or equal to the given raw score
    m = sum(score <= raw_score for score in raw_scores)
    
    # Calculate the percentile score using the formula (m/N) * 100
    percentile = (m / N) * 100
    
    return percentile

    #return (percentileofscore(raw_scores, raw_score) / 100) * 100

import pandas as pd

def merge_dataframes(df_list):
    # Create an empty DataFrame to store the combined results
    combined_df = pd.DataFrame()

    # Extract all unique percentiles from all DataFrames in df_list
    all_percentiles = sorted(set().union(*[df['Percentile_Score'] for df in df_list]), reverse=True)


    # Create a new DataFrame with Percentile_Score column
    combined_df['Percentile_Score'] = all_percentiles

    #combined_df['Percentile_Score'] = [round(percentile, 2) for percentile in all_percentiles]


    # Iterate through each DataFrame in df_list and map RawScores to the new DataFrame
    for i, df in enumerate(df_list):
        # Create a mapping of Percentile_Score to RawScore for the current DataFrame
        percentile_mapping = dict(zip(df['Percentile_Score'], df['RawScore']))

        # Create columns for RawScores based on the current index
        col_name = f'RawScore{i+1}'
        
        # Map RawScores to Percentile_Score in the new DataFrame
        combined_df[col_name] = combined_df['Percentile_Score'].map(percentile_mapping)

    return combined_df


def process_folder(folder_path):
    # List to store DataFrames for each file
    df_list = []

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Assuming files are CSV, you can adjust the read function accordingly
        df = pd.read_csv(file_path)

        # Calculate percentile scores and create a new column
        df['Percentile_Score'] = df['RawScore'].apply(
            lambda x: calculate_percentile_score(x, df['RawScore'])
        )
        print(df)

        # Append the DataFrame to the list
        df_list.append(df)

    return df_list

if __name__ == "__main__":
    folder_path = "E:/2023-2024/CSIR/Result/testNm/"  # Replace with your actual folder path
    df_list = process_folder(folder_path)
    print(1)
    combined_result = merge_dataframes(df_list)

    # Save the result to a new CSV file or do further processing as needed
    combined_result.to_csv("combined_result2.csv", index=False)
