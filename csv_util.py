import pandas as pd
import cleaning

def write_country_counts_csv(df: pd.DataFrame):
    pd.Series(df['Country'].value_counts()).to_csv("data/country_counts.csv", index=True)

def write_unique_countries_csv(df: pd.DataFrame):
    pd.Series(df['Country'].unique()).to_csv("data/unique_countries.csv", index=False)

def write_clean_country_counts_csv(df: pd.DataFrame):
    df['Country_Clean'] = df['Country'].apply(cleaning.clean_country)
    pd.Series(df['Country_Clean'].value_counts()).to_csv("data/clean_country_counts.csv", index=True)

def write_unique_clean_countries_csv(df: pd.DataFrame):
    df['Country_Clean'] = df['Country'].apply(cleaning.clean_country)
    print(sorted(list(df['Country_Clean'].unique())))
    pd.Series(sorted(list(df['Country_Clean'].unique()))).to_csv("data/unique_clean_countries.csv", index=False)

def write_other_currency_counts_csv(df: pd.DataFrame):
    pd.Series(df['Other Currency'].value_counts()).to_csv("data/other_currency_counts.csv", index=True)

def write_clean_other_currency_counts_csv(df: pd.DataFrame):
    df['Other Currency_Clean'] = df['Other Currency'].apply(cleaning.clean_other_currency)
    pd.Series(df['Other Currency_Clean'].value_counts()).to_csv("data/clean_other_currency_counts.csv", index=True)

def write_clean_data(df: pd.DataFrame):
    df.to_csv("data/clean_data.csv", index=False)
