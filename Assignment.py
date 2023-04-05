# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 22:13:56 2023

@author: pabas
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


def process_data(url):
    
    # Reading data from CSV file
    df = pd.read_csv(url, skiprows=4)

    # Defining the list of BRICS countries
    brics = ['China', 'Australia', 'India', 'South Africa', 'United Kingdom']

    # Define the list of preferred indicators
    preferred_indicators = ['Access to electricity (% of population)',
                          'Renewable electricity output (% of total electricity output)',
                          'Electricity production from renewable sources, excluding hydroelectric (% of total)']

    # Filtering the original dataframe by countries list and preferred indicators
    df_brics = df[(df['Country Name'].isin(brics)) & (
        df['Indicator Name'].isin(preferred_indicators))]

    # Select the preferred years and make them as columns
    years = ['2002', '2004', '2006', '2008', '2010']
    df_years = df_brics.loc[:, [
        'Country Name', 'Country Code', 'Indicator Name'] + years]

    # Removing of rows with missing values
    df_years.dropna(inplace=True)

    # Resetting the index
    df_years = df_years.reset_index(drop=True)

    # Transpose DataFrame without the index
    df_countries = df_years.set_index('Country Name').transpose()

    return df_years, df_countries


# Dataset file
url = 'climate_change (2).csv'

# define the function with the URL argument
df_years, df_countries = process_data(url)

# Print the two resulting dataframes
print(df_years)
print(df_countries)

# Saving the two DataFrames as CSV files
df_years.to_csv('df_years.csv', index=False)
df_countries.to_csv('df_countries.csv', index=False)

# Computing summary statistics for each indicator and country
stats = df_years.groupby(['Indicator Name', 'Country Name']).describe()

# Print the summary statistics for each indicator and country
print(stats)

# Group the data by Indicator Name
grouped_data = df_years.groupby(['Indicator Name'])

# Creating a bar chart for each indicator
for name, group in grouped_data:
    # Setting up the plot
    fig, ax = plt.subplots()
    # add a title name to the plot
    plt.title(name)
    ax.set_xticklabels(df_years['Country Name'].unique())
    ax.set_xticks(np.arange(len(df_years['Country Name'].unique())))
    ax.set_xlabel('Country Name')
    ax.set_ylabel(name)

    # Plot the data
    for i, year in enumerate(['2002', '2004', '2006', '2006', '2008']):
        ax.bar(np.arange(len(group['Country Name'].unique())) + i*0.15,
               group[year].values,
               width=0.15,
               label=year)

    # Add a legend
    ax.legend()

    # Show the plot
    plt.show()