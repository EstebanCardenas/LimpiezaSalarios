import pandas as pd

df = pd.read_csv("data/clean_data.csv")

pd.set_option('display.max_rows', None)    # None means "unlimited"
pd.set_option('display.max_columns', None)

print(df['Education Level'].isna().sum())
