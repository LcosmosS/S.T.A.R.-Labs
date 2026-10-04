import pandas as pd


# Load dataset
df_main = pd.read_csv('/home/pmqr7/path/to/your/pipe3d_data.csv')  # Ensure this path is correct


# Check available columns
print(df_main.columns)


# Ensure the column names match what you expect
df_main = df_main[['CATAID', 'log_SFR_Ha', 'log_Mass']]  # Modify these columns as needed


# Continue with your filtering and other steps
