import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def get_data_from_url(url):

    """
    Loads data from url into a pandas dataframe
    :param url: str - url of dataset
    :return: pandas dataframe of raw data 
    """

    df = pd.read_csv(url)
    return df


def process_data(df):

    """
    Performs basic cleaning by filling in null values
    with 0 and calculating 'gdp_per_capita' per country
    :param df: data
    :return: pandas dataframe of processed data
    """

    df.fillna(0, inplace=True)
    df["gdp_per_capita"] = df.apply(lambda row: row["gdp"] / row["population"] if row["population"] != 0 else 0, axis=1)
    return df

def filter_data(df, selected_locations):

    """
    Filters data by selecting only specified countries/continents
    :param df: dataset
    :param selected_locations: list of locations to filter in
    :return: pandas dataframe of filtered data with specified locations 
    """
    
    return df[df["country"].isin(selected_locations)]


def remove_non_countries(df):
    
    """
    Filters data by removing all datapoints with a non-country instance
    :param df: dataset
    :return: pandas dataframe of filtered data with only countries included
    """

    non_countries = ['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica',
                     'Africa (GCP)', 'Asia (GCP)', "Asia (excl. China and India)", "Central America (GCP)", "Europe (GCP)",
                     'Europe (excl. EU-27)', "Europe (excl. EU-28)", "European Union (27)", "European Union (27) (GCP)",
                     'European Union (28)', 'French Equatorial Africa (GCP)', 'French Guiana', 'French Polynesia', 'French West Africa (GCP)', 
                     'High-income countries', 'International transport', 'Kuwaiti Oil Fires (GCP)', 'Leeward Islands (GCP)', 'Low-income countries',
                     'Lower-middle-income countries', 'Micronesia (country)', 'Middle East (GCP)', 'Non-OECD (GCP)', 'North America (GCP)',
                     'North America (excl. USA)', 'OECD (GCP)', 'Oceania (GCP)', 'Ryukyu Islands (GCP)', 'Saint Martin (French part)', 'Sint Maarten (Dutch part)',
                     'South America (GCP)', 'Upper-middle-income countries']

    return df[df["country"].isin(non_countries) == False]


def plot_greenhouse_gas_emissions(df, ghg, year_range, selected_continents):
    
    """
    Creates a line chart of co2 emissions over time per continent
    :param df: dataset
    :param ghg: type of greenhouse gas
    :param year_range: selected time interval to display
    :param selected_continents: selected continents to display
    :return: streamlit line chart of specific greenhouse gas 
    """
    
    # Filter data based on continents
    filtered_df = filter_data(df, selected_continents)

    # Remove years with no values
    filtered_df = filtered_df.loc[filtered_df['year'].between(year_range[0], year_range[1])].dropna(subset=[ghg])

    # Create chart
    chart = alt.Chart(filtered_df).mark_line().encode(
        x=alt.X('year:Q', axis=alt.Axis(title="year")),
        y=alt.Y(f'{ghg}:Q', axis=alt.Axis(title=f"{ghg} emissions in metric tonnes")),
        color=alt.Color('country:N', title="Location")
    ).properties(title=f"{ghg} emissions over time", width=750, height=600).configure_legend(orient="top").configure_title(fontSize=24, anchor="start")

    # Show line chart
    st.write(chart)


# 
def plot_co2_vs_gdp(df, ghg, year_range, selected_countries):
    
    """
    Creates a scatter plot of co2 emissions vs gdp per capita per selected countries
    :param df: dataset
    :param ghg: type of greenhouse gas
    :param year_range: selected year range, will convert to year to display
    :param selected_countries: selected countries to display
    :return: streamlit scatter chart of specific greenhouse gas
    """

    # filter_df based on maximum year on slider year range and selected countries in multiselect box
    filtered_df = df[df['year'] == max(year_range)]
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

    # Get the mean gdp_per_capita per country based on the selected year range
    mean_df = filtered_df[filtered_df['year'] == max(year_range)].groupby('country').mean().reset_index()
    mean_df = mean_df[mean_df["gdp_per_capita"] > 0]

    if mean_df["gdp_per_capita"].empty:
        st.write("No data available for the selected year.")
        return alt.Chart(pd.DataFrame({'x': [], 'y': []})).mark_circle().encode()

    # Create a scatter plot with the y-axis being the mean 'co2' value and the x-axis being the mean 'gdp_per_capita' value
    chart = alt.Chart(mean_df).mark_circle(size=60).encode(
        alt.X('gdp_per_capita:Q', axis=alt.Axis(title='GDP per capita')),
        alt.Y(f'{ghg}:Q', axis=alt.Axis(title='CO2 Emissions (metric tons per capita)')),
        color=alt.Color('country:N', title="Location"),
        size=alt.Size('population:Q', legend=None),
        tooltip=['country', f'{ghg}', 'gdp_per_capita']
    ).properties(title=f"{ghg} emissions vs GDP per capita in {max(year_range)}", width=700, height=500).configure_legend(orient="top").configure_title(fontSize=24, anchor="start")
    
    st.write(chart)


def plot_co2_sources(df, year_range, selected_sources, selected_locations):

    """
    Creates a grouped bar char of co2 sources per country/continent
    :param df: dataset
    :param ghg: type of greenhouse gas
    :param year_range: selected year range, will convert to year to display
    :param selected_locations: selected countries/continents to display
    :return: streamlit grouped bar chart of specified co2 emission source per location
    """

    # filter_df based on maximum year on slider and selected countries in multiselect box
    filtered_df = df[df['year'] == max(year_range)]
    filtered_df = filter_data(df, selected_locations)

    chart = alt.Chart(filtered_df).transform_fold(selected_sources, as_=["key", "value"]).mark_bar().encode(
        x=alt.X("key:N", axis=None),
        y=alt.Y("value:Q", title = "emissions in million tonnes"),
        color=alt.Color("key:N", title=None),
        column=alt.Column("country", title=None, header=alt.Header(labelOrient=("bottom")))
    ).properties(title="CO2 emissions by source").configure_legend(orient="top").configure_title(fontSize=24, anchor="start")

    st.write(chart)