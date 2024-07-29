import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json


@st.cache
def load_data(fp):
    print('Running load_data...')

    # read in the csv via the link
    df = pd.read_csv(fp)

    return(df)


st.set_page_config(
    page_title="Original Data"
    )


st.header("Original Video Game Data")

st.write("This is the original data.")

original_data = "https://raw.githubusercontent.com/HA-work/esrb_project/main/data/video_games_esrb_rating.csv"


#df = load_data(original_data)

df = pd.read_csv('data/video_games_esrb_rating.csv')




st.dataframe(data=df)