import pandas as pd
import csv_util
import cleaning
import conversion_api
import conversion_cache
from api_key import API_KEY

df = pd.read_csv("data/data.csv")

df.rename(columns={
    "How old are you?": "Age",
    "What industry do you work in?": "Industry",
    "Job title": "Job Title",
    "If your job title needs additional context, please clarify here:": "Job Title Context",
    "What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)": "Salary",
    "How much additional monetary compensation do you get, if any (for example, bonuses or overtime in an average year)? Please only include monetary compensation here, not the value of benefits.": "Bonus",
    "Please indicate the currency": "Currency",
    "If \"Other,\" please indicate the currency here: ": "Other Currency",
    "If your income needs additional context, please provide it here:": "Income Context",
    "What country do you work in?": "Country",
    "If you're in the U.S., what state do you work in?": "US State",
    "What city do you work in?": "City",
    "How many years of professional work experience do you have overall?": "Years of Experience",
    "How many years of professional work experience do you have in your field?": "Years of Experience in Field",
    "What is your highest level of education completed?": "Education Level",
    "What is your gender?": "Gender",
    "What is your race? (Choose all that apply.)": "Race",
}, inplace=True)

def clean_data(df):
    df['Country'] = df['Country'].map(cleaning.clean_country)
    df['City'] = df['City'].map(cleaning.clean_city)
    df['Currency'] = df['Currency'].map(lambda x: 'AUD' if x == 'AUD/NZD' else x)
    df['Other Currency'] = df['Other Currency'].map(cleaning.clean_other_currency)
    # Clean both Salary and Bonus
    for col in ['Salary', 'Bonus']:
        # Convert to string first to handle any existing NaNs, then clean
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)

def calculate_salary_in_cop(df, use_cache=True):    
    # Get effective currency for each row
    effective_currencies = df['Other Currency'].fillna(df['Currency'])
    unique_currencies = effective_currencies.unique()

    # Get rates map
    rates_map = {}
    for curr in unique_currencies:
        if pd.isna(curr): continue
        if curr == 'Other': continue
        if curr == 'HHV': continue
        
        rate = conversion_cache.get_cached_rate(curr) if use_cache else None
        if rate is None:
            print(f"No cached rate found for {curr}, calling API...")
            rate = conversion_api.get_conversion_rate(curr, 'COP')
            if rate is not None:
                conversion_cache.set_cached_rate(curr, rate)
        rates_map[curr] = rate

    # Apply the conversion
    df.loc[:, 'Salary COP'] = df['Salary'] * effective_currencies.map(rates_map)
    df.loc[:, 'Bonus COP'] = df['Bonus'] * effective_currencies.map(rates_map)
    df.loc[:, 'Converted To COP'] = df['Salary COP'].notna()

def calculate_total_compensation(df):
    df.loc[:, 'Total Compensation COP'] = df['Salary COP'] + df['Bonus COP']

if __name__ == '__main__':
    clean_data(df)
    # Start of COP salary calculation
    conversion_cache.load_cache()
    calculate_salary_in_cop(df)
    conversion_cache.save_cache()
    # End of COP salary calculation
    calculate_total_compensation(df)
    # Write new clean data
    csv_util.write_clean_data(df)
