import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(
    page_title="About"
    )


st.write("The model made for the project was a Random Forest classifier.")

st.write("It was selected as it was the best performing out of the several models attempted")

st.write("It was trained on about 2200 rows of data.")



cleaned_data = "https://raw.githubusercontent.com/HA-work/esrb_project/main/data/cleaned_games.csv"


df = pd.read_csv(cleaned_data)


st.subheader('First 5 rows of the data after some cleaning.')

st.dataframe(df[:5])




st.write("The data is composed of games along with their ratings and content descriptions.")

st.write("The model takes in these content descriptions to try and see if there is a pattern for how games are given their age rating.")

st.write("The model was made with the default hyper parameters as after testing multiple variations using CV Grid Search a noticable improvement was not found.")

st.write("The model achieved an accuracy, f1-score and recall of 87%")

st.write("After this the model was then trained on all the data to create the final model.")


