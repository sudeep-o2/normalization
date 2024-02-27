# fo percentile gen for all files  

"""import os
import pandas as pd
from scipy.stats import percentileofscore

def calculate_percentile_score(raw_score, raw_scores):
    return (percentileofscore(raw_scores, raw_score) / 100) * 100

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
    folder_path = "E:/2023-2024/CSIR/Result/testNm/" # Replace with your actual folder path
    process_folder(folder_path)"""

import os
import pandas as pd
from scipy.stats import percentileofscore

def calculate_percentile_score(raw_score, raw_scores):
    #return (percentileofscore(raw_scores, raw_score) / 100) * 100

    N = len(raw_scores)
    
    # m is the count of candidates with raw scores less than or equal to the given raw score
    m = sum(score <= raw_score for score in raw_scores)
    
    # Calculate the percentile score using the formula (m/N) * 100
    percentile = (m / N) * 100
    
    return percentile

def process_folder(folder_path):
    # List to store DataFrames for each file
    df_list = []

    c=1
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Assuming files are CSV, you can adjust the read function accordingly
        df = pd.read_csv(file_path)

        # Calculate percentile scores and create a new column
        df['Percentile_Score'] = df['RawScore'].apply(
            lambda x: calculate_percentile_score(x, df['RawScore'])
        )

        #print(df)
        output_file_path = f'output_shift_{c}_with_percent.csv'
        c+=1
        df.to_csv(output_file_path, index=False)
        # Append the DataFrame to the list
        df_list.append(df)

    return df_list



if __name__ == "__main__":
    folder_path = "E:/2023-2024/CSIR/Result/testNm/" # Replace with your actual folder path
    process_folder(folder_path)