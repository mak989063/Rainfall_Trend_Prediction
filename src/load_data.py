import pandas as pd

def load_cleaned_data(filepath="data/kerala_rainfall_cleaned.csv"):
    return pd.read_csv(filepath)