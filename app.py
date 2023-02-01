from utils import *
import streamlit as st

st.set_page_config(page_title="GHG Emissions Dashboard", layout="wide")

url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
df = get_data_from_url(url)
df = process_data(df)

# year slider, set constraints to 1990 and 2018 as this range contains the most complete data
year_range = st.sidebar.slider("Year Range", min_value=int(1990), max_value=int(2018), value=(int(1990), int(2018)), step=1)

# multiselect box
selected_continents = st.sidebar.multiselect("Select continents", options=['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica'], default=['Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America'])

#multiselect box for countries
selected_countries = st.sidebar.multiselect("Select countries for GHG vs GDP Per Capita", options=remove_non_countries(df)["country"].unique(), default = ["China", "India", "Philippines", "Vietnam", "Belgium", "France", "Spain"])

#multiselect box for co2 emission sources
selected_sources = st.sidebar.multiselect("Select CO2 emission sources", options=["coal_co2", "gas_co2", "flaring_co2", "oil_co2", "other_industry_co2", "cement_co2"], default=["coal_co2", "gas_co2", "flaring_co2", "oil_co2", "other_industry_co2", "cement_co2"])
st.title("Greenhouse Gas Emissions Over Time")

col1, col2 = st.columns(2, gap="medium")

with col1:
    plot_greenhouse_gas_emissions(df, "total_ghg", year_range, selected_continents)
    plot_greenhouse_gas_emissions(df, "methane", year_range, selected_continents)

with col2:
    plot_greenhouse_gas_emissions(df, "co2", year_range, selected_continents)
    plot_greenhouse_gas_emissions(df, "nitrous_oxide", year_range, selected_continents)

st.title("Total greenhouse gas emissions vs GDP per Capita")

col1, col2 = st.columns(2, gap="medium")

with col1:
    plot_co2_vs_gdp(df, "total_ghg", year_range, selected_countries)
    plot_co2_vs_gdp(df, "methane", year_range, selected_countries)

with col2:
    plot_co2_vs_gdp(df, "co2", year_range, selected_countries)
    plot_co2_vs_gdp(df, "nitrous_oxide", year_range, selected_countries)

st.title("CO2 emissions by source")

col1, col2 = st.columns(2, gap="medium")

with col1:
    plot_co2_sources(df, year_range, selected_sources, selected_continents)

with col2:
    plot_co2_sources(df, year_range, selected_sources, selected_countries)