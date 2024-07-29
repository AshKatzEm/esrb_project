import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json

# maybe change how the data is accessed to save memory






@st.cache
def load_data(fp):
    print('Running load_data...')

    # read in the csv via the link
    df = pd.read_csv(fp)

    return(df)


st.set_page_config(
    page_title="Cleaned Data"
    )


st.header("Cleaned Video Game Data")

#

st.write("This is the data after removing duplicates, fixing spelling errors and correcting wrong data values.")

st.write("Additional features were also added like the Number of Descriptors")


cleaned_data = "https://raw.githubusercontent.com/HA-work/esrb_project/main/data/cleaned_games.csv"


#df = load_data(cleaned_data)

df = pd.read_csv('data/cleaned_games.csv')

# not sure which is faster or if it matters


st.dataframe(data=df)