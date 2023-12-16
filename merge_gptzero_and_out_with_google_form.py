# Re-importing pandas as the code execution state was reset
import pandas as pd

# Reopening both provided CSV files
file_path_essays = 'essays_merged_dataframe.csv'
file_path_google_form = 'google_form_export.csv'

# Loading the data from each file
df_essays = pd.read_csv(file_path_essays)
df_google_form = pd.read_csv(file_path_google_form)

# Inspecting the first few rows of both dataframes to understand their structure and identify the relevant columns
df_essays_head = df_essays.head()
df_google_form_head = df_google_form.head()

df_essays_head, df_google_form_head

# Converting the 'Parent Folder' column in df_essays to a datetime format
df_essays['Parent Folder'] = pd.to_datetime(df_essays['Parent Folder'], format='%m-%d-%Y %H_%M_%S', errors='coerce')

# Converting the 'Timestamp' column in df_google_form to a datetime format
df_google_form['Timestamp'] = pd.to_datetime(df_google_form['Timestamp'], format='%m/%d/%Y %H:%M:%S', errors='coerce')

# Merging the dataframes on the converted date columns
merged_df = pd.merge(df_essays, df_google_form, left_on='Parent Folder', right_on='Timestamp', how='inner')

# Displaying the first few rows of the merged dataframe
print(merged_df.head())
# Exporting the merged dataframe to a CSV file
merged_csv_path = 'essays_merged_dataframe_with_google_form.csv'
merged_df.to_csv(merged_csv_path, index=False)