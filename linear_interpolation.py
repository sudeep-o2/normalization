import os
import pandas as pd
import numpy as np


def calculate_percentile_score(df):
    """Calculates the percentile score for each row in a DataFrame."""
    df["Percentile Score"] = df.groupby("RawScore")["RawScore"].transform(
        pd.Series.rank, pct=True
    ) * 100
    return df


def pullback_to_marks(df):
    """Pullback percentiles to marks for each session and create Raw Score columns."""
    df_grouped = df.groupby("Percentile Score", sort=False)["RawScore"].max().reset_index()
    df_grouped.columns = ["Percentile Score", "Raw Score S1"]

    # Ensure identical labels before merging
    df_grouped = df_grouped.sort_values(by="Percentile Score")
    df = df.sort_values(by="Percentile Score")

    for i in range(1, len(df.columns) - 2):  # Number of shifts - 2 (candidate and percentile)
        # Check if the column exists before accessing and handle missing values
        if f"Raw Score S{i + 1}" not in df_grouped.columns:
            df_grouped[f"Raw Score S{i + 1}"] = np.nan

        df = pd.merge(
            df,
            df_grouped[[f"Percentile Score", f"Raw Score S{i + 1}"]],
            how="left",
            left_on="Percentile Score",
            right_on="Percentile Score",
        )

    return df


def interpolate_missing_scores(df, column):
    """Fills missing entries in a Raw Score column using linear interpolation."""
    for index, row in df.iterrows():
        if pd.isna(row[column]):
            # Handle missing values (e.g., return specific value or raise an error)
            # Option 1: Replace with a specific value (e.g., -1)
            df.loc[index, column] = -1
            # Option 2: Raise an error
            # raise ValueError("Missing value encountered in column:", column)
            continue  # Skip this iteration to avoid further calculations

        # Ensure numerical data types before calculations
        data = df[column].dropna().astype(float)  # Convert to float
        x_data = df["Percentile Score"].dropna()
        target = row["Percentile Score"]
        df.loc[index, column] = interpolate(data, x_data, target)
    return df


def interpolate(data, x_data, target):
    """Performs linear interpolation between two points."""
    if len(data) == 1:
        return data.iloc[0]
    data_sorted = pd.DataFrame({"data": data, "x_data": x_data}).sort_values("x_data")
    i = data_sorted.index[data_sorted["x_data"] <= target].max()
    if i == len(data_sorted) - 1:
        return data_sorted.iloc[-1]["data"]
    x1, x2 = data_sorted.iloc[i]["x_data"], data_sorted.iloc[i + 1]["x_data"]
    y1, y2 = data_sorted.iloc[i]["data"], data_sorted.iloc[i + 1]["data"]
    return y1 + ((y2 - y1) / (x2 - x1)) * (target - x1)


def process_folder(folder_path):
    """Processes a folder containing shift data, calculating percentiles, pulling back marks, and interpolating."""
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder_path, filename))
            # Ensure numerical data type for "Raw Score" before calculations
            df["RawScore"] = pd.to_numeric(df["RawScore"], errors="coerce")  # Handle non-numeric values
            df = calculate_percentile_score(df.copy())  # Avoid modifying original DataFrame
            df = pullback_to_marks(df)
            for column in df.columns[2:]:  # Skip "candidate" and "Percentile Score" columns
                df = interpolate_missing_scores(df.copy(), column)  # Avoid modifying original DataFrame
                
 # Avoid modifying original DataFrame
            output_path = os.path.join(folder_path, f"processed_{filename}")
            df.to_csv(output_path, index=False)
            print(f"Processed file: {filename}, saved to: {output_path}")


if __name__ == "__main__":
    folder_path = "E:/2023-2024/CSIR/Result/testNm/"  # Replace with your actual folder path
    process_folder(folder_path)

