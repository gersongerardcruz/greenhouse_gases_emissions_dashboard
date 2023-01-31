import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np

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

def filter_continents(df):
    # Filter data based on continents
    continents = ['Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica']
    return df[df["country"].isin(continents)]

def remove_non_countries(df):
    # Remove non-countries to get country level information
    non_countries = ['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica'
                     'Africa (GCP)', 'Asia (GCP)', "Asia (excl. China and India)", "Central America (GCP)", "Europe (GCP)",
                     'Europe (excl. EU-27)', "Europe (excl. EU-28)", "European Union (27)", "European Union (27) (GCP)",
                     'European Union (28)', 'French Equatorial Africa (GCP)', 'French Guiana', 'French Polynesia', 'French West Africa (GCP)', 
                     'High-income countries', 'International transport', 'Kuwaiti Oil Fires (GCP)', 'Leeward Islands (GCP)', 'Low-income countries',
                     'Lower-middle-income countries', 'Micronesia (country)', 'Middle East (GCP)', 'Non-OECD (GCP)', 'North America (GCP)',
                     'North America (excl. USA)', 'OECD (GCP)', 'Oceania (GCP)', 'Ryukyu Islands (GCP)', 'Saint Martin (French part)', 'Sint Maarten (Dutch part)',
                     'South America (GCP)', 'Upper-middle-income countries']
    return df[df["country"].isin(non_countries) == False]

# Create line chart of co2 emissions over time per continent
def plot_co2_emissions(df):
    st.title("CO2 Emissions Over Time")
    
    # Filter data based on countries
    filtered_df = filter_data(df, selected_countries)

    # Remove years with no values
    filtered_df = filtered_df.loc[filtered_df['year'].between(year_range[0], year_range[1])].dropna(subset=['co2'])

    # Create chart
    chart = alt.Chart(filtered_df).mark_line().encode(
        x='year:Q',
        y='co2:Q',
        color='country:N'
    ).properties(width=900, height=500)

    # Show line chart
    return chart



# Create scatter plot of co2 vs gdp per capita
def plot_co2_vs_gdp(df, year_range):
    st.title("CO2 emissions vs GDP per Capita")

    # filter_df based on maximum year on slider and selected countries in multiselect box
    filtered_df = df[df['year'] == max(year_range)]
    filtered_df = remove_non_countries(filtered_df)

    # Get the mean gdp_per_capita per country based on the selected year range
    mean_df = filtered_df[filtered_df['year'] == max(year_range)].groupby('country').mean().reset_index()

    # Create a scatter plot with the y-axis being the mean 'co2' value and the x-axis being the mean 'gdp_per_capita' value
    chart = alt.Chart(mean_df).mark_circle(size=60).encode(
        alt.X('gdp_per_capita:Q', axis=alt.Axis(title='GDP per capita')),
        alt.Y('co2:Q', axis=alt.Axis(title='CO2 Emissions (metric tons per capita)')),
        color=alt.Color('country:N', legend=None),
        size=alt.Size('population:Q', legend=None),
        tooltip=['country', 'co2', 'gdp_per_capita']
    ).properties(width=900, height=500)
    
    return chart

def plot_co2_sources(df, year_range):
    st.title("CO2 emissions by source per continent")

    # filter_df based on maximum year on slider and selected countries in multiselect box
    filtered_df = df[df['year'] == max(year_range)]
    filtered_df = filter_data(df, selected_countries)

    sources = ["country", "coal_co2", "gas_co2", "flaring_co2", "oil_co2", "other_industry_co2", "cement_co2"]
    filtered_df = filtered_df[sources]

    chart = alt.Chart(filtered_df).transform_fold(sources, as_=["key", "value"]).mark_bar().encode(
        x=alt.X("key:N", axis=None),
        y=alt.Y("value:Q", title = "emissions in million tonnes"),
        color=alt.Color("key:N", title=None),
        column=alt.Column("country", title=None, header=alt.Header(labelOrient=("bottom")))
    )

    return chart

def plot_other_greenhouse_gases(df, year_range):
    st.title("Other greenhouse gas emissions per continent")

    # filter_df based on maximum year on slider and selected countries in multiselect box
    filtered_df = df[df['year'] == max(year_range)]
    filtered_df = filter_data(df, selected_countries)

    sources = ["country", "methane", "nitrous_oxide"]
    filtered_df = filtered_df[sources]

    chart = alt.Chart(filtered_df).transform_fold(sources, as_=["key", "value"]).mark_bar().encode(
        x=alt.X("key:N", axis=None),
        y=alt.Y("value:Q", title = "emissions in million tonnes"),
        color=alt.Color("key:N", title=None),
        column=alt.Column("country", title=None, header=alt.Header(labelOrient=("bottom")))
    )

    return chart 


url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
df = get_data_from_url(url)
df = clean_data(df)

st.write(df.head()) 

# year slider
year_range = st.slider("Year Range", min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=(int(df['year'].min()), int(df['year'].max())), step=1)

# multiselect box
selected_countries = st.multiselect("Select countries", options=['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica'], default=['Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America'])

chart0 = plot_co2_emissions(df)
chart1 = plot_co2_vs_gdp(df, year_range)
chart2 = plot_co2_sources(df, year_range)
chart3 = plot_other_greenhouse_gases(df, year_range)

st.write(alt.hconcat(chart0, chart1, chart2, chart3))