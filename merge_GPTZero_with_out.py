import pandas as pd
# Load the first CSV, which comes from GPTZero
df_160 = pd.read_csv("160_essays_GPTZeroExport-12_13_2023.csv")

# Load the second CSV, which comes from parse_folders_out_and_files
df_out14 = pd.read_csv('out14.csv')

# Merging the dataframes based on the "File Name" column in df_160 and the "Hashed Filename" column in df_out14
merged_df = pd.merge(df_160, df_out14, left_on="File Name", right_on="Hashed Filename")

# Checking the first few rows of the merged dataframe
merged_df_head = merged_df.head()
print(merged_df_head)
# Exporting the merged dataframe to a CSV file
merged_csv_path = 'essays_merged_dataframe.csv'
merged_df.to_csv(merged_csv_path, index=False)