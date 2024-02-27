import os
import pandas as pd
import numpy as np
from scipy.stats import percentileofscore


def calculate_percentile_scores(df):
    
    """Calculates the percentile score for each row in a DataFrame."""
    df["Percentile Score"] = df.groupby("RawScore")["RawScore"].transform(
        pd.Series.rank, pct=True
    ) * 100
    return df


def create_collated_table(dfs):
    """
    Creates a collated table with percentile scores and Raw Scores from each file.

    Args:
        dfs (list): A list of DataFrames, each containing data from a single file.

    Returns:
        pd.DataFrame: The collated table with percentile scores and Raw Scores.
    """

    all_candidates = [df["Candidate"].iloc[0] for df in dfs]  # List of candidates from all files
    unique_percentiles = sorted(set(df["Percentile Score"] for df in dfs))  # Unique percentiles across all files

    # Create the collated DataFrame structure
    collated_data = {"Percentile Score": unique_percentiles}
    for candidate in all_candidates:
        collated_data[candidate] = np.nan

    collated_df = pd.DataFrame(collated_data)

    # Fill in marks based on percentile matches for each file
    for df in dfs:
        df_candidate = df["Candidate"].iloc[0]  # Get the candidate name for this file
        df_percentiles = df["Percentile Score"].tolist()
        df_raw_scores = df["Raw Score"].tolist()

        for i, percentile in enumerate(df_percentiles):
            if percentile in collated_df["Percentile Score"]:
                collated_df.loc[collated_df["Percentile Score"] == percentile, df_candidate] = df_raw_scores[i]

    return collated_df


def process_folder(folder_path):
    """Processes a folder containing CSV files and creates a collated table."""
    dfs = []
    x=1
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder_path, filename))
            df["RawScore"] = pd.to_numeric(df["RawScore"], errors="coerce")  # Handle non-numeric values
            df = calculate_percentile_scores(df)
            output_file_path = f'output_shift_{x}_with_marks.csv'
            x+=1
            df.to_csv(output_file_path, index=False)
            #print(df)
            dfs.append(df)

    collated_df = create_collated_table(dfs)
    output_path = os.path.join(folder_path, "collated_data.csv")
    collated_df.to_csv(output_path, index=False)
    print(f"Collated data saved to: {output_path}")







if __name__ == "__main__":
    folder_path = "E:/2023-2024/CSIR/Result/testNm/" # Replace with your actual folder path
    process_folder(folder_path)
