"""
RealClearPolling Data Loader

This script is a collection of Python modules that load data from RealClearPolling.
It provides functions to fetch and process polling data from various sources.

Author: Robert Feldstein
Date: 2-28-24
"""

# Import necessary modules
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import plotly.express as px

# Suppress a specific warning
warnings.simplefilter("ignore", category=FutureWarning)

#Data urls
base_url = "https://www.realclearpolling.com/polls/"
two_candidate = "president/general/2024/trump-vs-biden"
three_candidate = "president/general/2024/trump-vs-biden-vs-kennedy"
five_candidate = "president/general/2024/trump-vs-biden-vs-kennedy-vs-west-vs-stein"
jbdturl = base_url + two_candidate
jbkturl = base_url + three_candidate
fivecanurl = base_url + five_candidate

def get_poll_urls():
    """
    Retrieves the URLs of the polling data from RealClearPolitics.

    Returns:
    dict: A dictionary containing the URLs of the polling data.
    """
    return {"two_candidate": jbdturl, "three_candidate": jbkturl, "five_candidate": fivecanurl}

#Function to get the data and load it into a dataframe

def get_poll_data(url = jbdturl):
    """
    Retrieves poll data from a given URL and returns it as a pandas DataFrame.

    Parameters:
    url (str): The URL of the webpage containing the poll data.

    Returns:
    pandas.DataFrame: A DataFrame containing the extracted poll data.
    """
    
    # Create a webdriver instance and get the page source
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    # Get the page source after dynamic content has loaded
    html_content = driver.page_source

    # Close the webdriver
    driver.quit()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html5lib')

    # Now you can extract the table data using the same approach as before
    table = soup.find_all('table')

    if len(table)==2:
        table = table[1]
    else:
        table = table[0]

    table_data = []
    for row in table.find_all('tr'):
        row_data = [cell.text.strip() for cell in row.find_all(['td','th'])]
        table_data.append(row_data)
    df = pd.DataFrame(table_data[2:], columns=table_data[0])
    return df

def clean_data(df):
    """
    Cleans the given DataFrame by performing various data transformations.

    Args:
        df (pandas.DataFrame): The DataFrame to be cleaned.

    Returns:
        pandas.DataFrame: The cleaned DataFrame.
    """
    df = df.copy()
    current_year = str(datetime.now().year)
    prev_year = str(datetime.now().year-1)
    df["Difference"] = df["Trump (R)"].astype(float) - df["Biden (D)"].astype(float)
    df["Type of Voter"] = df["sample"].str.split(" ").str[1]
    df["Sample Size"] = pd.to_numeric(df["sample"].str.split(" ").str[0], errors="coerce").fillna(0).astype(int)
    df["End Date"] = df["date"].str.split("-").str[1] 
    df["Poll Month"] = df["date"].str.split("-").str[1].str.split("/").str[0]
    df["Poll Month"] = df["Poll Month"].astype(int)
    first_dec = df[df["Poll Month"]==12].index[0]
    df["Year"] = [current_year]*first_dec + [prev_year]*(len(df)-first_dec)
    df["End Date"] = df["End Date"] + "/" + df["Year"]
    df["End Date"] = np.array(pd.to_datetime(df["End Date"], format="mixed"))
    df = df[df["Type of Voter"].isin(["RV", "LV"])]
    for can_name in ["Biden (D)", "Trump (R)","Kennedy (I)", "West (I)", "Stein (G)"]:
        if can_name in df.columns:
            df[can_name] = df[can_name].astype(float)

    df["Days Since 01-01-23"] = (df["End Date"] - pd.to_datetime("01-01-23")).dt.days
    return df


