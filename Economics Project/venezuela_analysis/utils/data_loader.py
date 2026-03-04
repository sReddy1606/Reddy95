import pandas as pd
import wbgapi as wb
import streamlit as st

# 1. World Bank Macroeconomic Data
@st.cache_data(ttl=3600)
def fetch_venezuela_macro():
    """
    Fetches GDP per capita and Inflation data from World Bank.
    Uses transposition to ensure compatibility with Plotly.
    """
    indicators = {
        'NY.GDP.PCAP.CD': 'GDP_Per_Capita',
        'FP.CPI.TOTL.ZG': 'Inflation_Rate'
    }
    try:
        # Fetching data for Venezuela (VEN) from 1990 to 2024
        df = wb.data.DataFrame(list(indicators.keys()), 'VEN', 
                               time=range(1990, 2025), numericTimeKeys=True)
        
        if df.empty:
            return pd.DataFrame()

        # Transpose so indicators are columns and years are rows
        df = df.T.rename(columns=indicators)
        df.index = df.index.set_names('Year')
        
        # Clean data: Fill minor gaps using linear interpolation
        df = df.interpolate(method='linear').ffill().bfill()
        return df
    except Exception as e:
        st.error(f"Error fetching World Bank data: {e}")
        return pd.DataFrame()

# 2. Historical Poverty Milestones (1920 - Present)
@st.cache_data
def fetch_poverty_history():
    """
    Returns specific historical poverty data points for Venezuela.
    Depicts the 'U-Turn' from a wealthy nation to widespread poverty.
    """
    data = {
        'Year': [1920, 1950, 1970, 1998, 2013, 2021, 2024],
        'Poverty_Rate': [70, 35, 25, 45, 30, 94, 82],
        'Context': [
            'Pre-Oil Boom', 'Richest in LA', 'Golden Era', 
            'Political Shift', 'Oil Price Peak', 
            'Hyperinflation Crisis', 'Moderate Recovery'
        ]
    }
    return pd.DataFrame(data)

# 3. Oil Production History (Milestones & Labels)
@st.cache_data
def get_oil_production_history():
    """
    Returns the history of oil production in Million Barrels Per Day (MBPD).
    Captures the peak and subsequent institutional collapse.
    """
    data = {
        'Year': [1920, 1945, 1970, 1985, 1998, 2013, 2020, 2024],
        'Production': [0.1, 1.0, 3.7, 1.7, 3.3, 2.5, 0.4, 0.86],
        'Label': [
            'Initial Exports', 'WWII Demand', 'Historical Peak', 
            'Nationalization', 'PDVSA Expansion', 'Succession Crisis', 
            'Systemic Collapse', 'Chevron/Current'
        ]
    }
    return pd.DataFrame(data)

# 4. Global Oil Comparison (Reserves vs. Production)
@st.cache_data
def get_global_comparison_data():
    """
    Compares Venezuela (#1 Reserves) against the Top 5 Global Producers.
    Highlights the efficiency gap (The Paradox).
    """
    data = {
        'Country': ['Venezuela', 'USA', 'Saudi Arabia', 'Russia', 'Canada', 'Iraq'],
        'Reserves_Billion_Bbl': [303.2, 55.2, 267.2, 80.0, 163.6, 145.0],
        'Production_MBPD': [0.86, 21.9, 11.1, 10.7, 5.7, 4.4]
    }
    return pd.DataFrame(data)

# 5. Simulation Baseline Data (The Venezuelan Reality)
@st.cache_data
def get_venezuela_simulation_data():
    """
    Provides specific indexed data for the simulator to show 
    the severity of the economic contraction.
    """
    # GDP Index (2013 = 100)
    gdp_index = pd.DataFrame({
        'Year': [1998, 2008, 2013, 2016, 2018, 2020, 2024],
        'Value': [70, 95, 100, 75, 45, 20, 25]
    })
    return gdp_index