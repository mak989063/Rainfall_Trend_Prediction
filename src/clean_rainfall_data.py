
import pandas as pd


def clean_rainfall_data(filepath):
    df = pd.read_excel(filepath)
    df = df.dropna(how="all")  # drop completely empty rows
    df.columns = [col.strip() for col in df.columns]
    # Convert year columns to int if necessary
    df = df.melt(id_vars=["District"], var_name="Year", value_name="Rainfall")
    df["Year"] = df["Year"].astype(int)
    df["Rainfall"] = pd.to_numeric(df["Rainfall"], errors='coerce')
    df = df.dropna(subset=["Rainfall"])
    return df
