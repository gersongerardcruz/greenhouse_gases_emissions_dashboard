import streamlit as st
import pandas as pd
import altair as alt

def get_data_from_url(url: str):
    df = pd.read_csv(url)
    return df

def clean_data(df):
    df.fillna(0, inplace=True)
    df["gdp_per_capita"] = df.apply(lambda row: row["gdp"] / row["population"] if row["population"] != 0 else 0, axis=1)
    return df

def filter_data(df, selected_countries):
    # Filter data based on selected countries
    return df[df["country"].isin(selected_countries)]

def plot_co2_emissions(df):
    st.title("CO2 Emissions Over Time")
    
    # Filter data based on countries
    selected_countries = st.multiselect("Select countries", options=['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica'], default=["World"])
    filtered_df = filter_data(df, selected_countries)
    
    # Current year 
    current_year = pd.to_datetime("today").year

    # Create line chart
    year_range = st.slider("Year Range", min_value=int(df['year'].min()), max_value=int(current_year), value=(int(df['year'].min()), int(current_year)), step=1)
    chart = alt.Chart(filtered_df).mark_line().encode(
        x='year:Q',
        y='co2:Q',
        color='country:N'
    ).properties(width=900).interactive()

    # Show line chart
    st.altair_chart(chart.transform_filter(alt.datum.year >= year_range[0]).transform_filter(alt.datum.year <= year_range[1]))


url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
df = get_data_from_url(url)
df = clean_data(df)

st.write(df)
plot_co2_emissions(df)