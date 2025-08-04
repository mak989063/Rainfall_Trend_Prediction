import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from src.load_data import load_cleaned_data

st.set_page_config(page_title="Kerala Rainfall Trends", layout="wide")
st.title("🌧 Kerala District Rainfall Trends Dashboard")

# Load data
df = load_cleaned_data()
df.columns = df.columns.str.strip()  # Strip any leading/trailing spaces

# Drop existing 'Rainfall' column if it exists to avoid melt conflict
if 'Rainfall' in df.columns:
    df = df.drop(columns=['Rainfall'])

# Reshape the data from wide to long format for monthly trend
try:
    df_melted = df.melt(
        id_vars=["District", "Year"],
        value_vars=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        var_name="Month",
        value_name="Rainfall"
    )
except Exception as e:
    st.error(f"❌ Failed to reshape data: {e}")
    st.stop()

# Sidebar filters
districts = df_melted["District"].unique()
selected_districts = st.sidebar.multiselect("Select District(s):", options=districts, default=["Palakkad"])
year_range = st.sidebar.slider("Select Year Range:", int(df_melted['Year'].min()), int(df_melted['Year'].max()), (2020, 2025))

# Filter data
filtered = df_melted[
    df_melted['District'].isin(selected_districts) &
    df_melted['Year'].between(*year_range)
]

# Handle empty data
if filtered.empty:
    st.warning("⚠️ No data available for selected filters. Please adjust the district or year range.")
    st.stop()

# Line chart
st.subheader("📈 Rainfall Trend (Monthly)")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered, x="Year", y="Rainfall", hue="District", marker="o", ax=ax)
ax.set_ylabel("Rainfall (mm)")
st.pyplot(fig)

# District-wise total summary
st.subheader("🗺️ District-wise Rainfall Summary")
total_rainfall = filtered.groupby("District")["Rainfall"].sum().reset_index()
total_rainfall = total_rainfall.rename(columns={"Rainfall": "Annual_Rainfall (mm)"})
st.dataframe(total_rainfall.sort_values(by="Annual_Rainfall (mm)", ascending=False))
