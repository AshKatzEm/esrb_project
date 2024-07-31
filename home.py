import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import re
# added this to try and save resources

# not sure why I got the mutation warning when I do not change the model

@st.cache_resource(allow_output_mutation=True)
def load_model():
	return pickle.load(open("models/final_model_releasedate.pkl", 'rb'))



st.set_page_config(
    page_title="ESRB Prediction",
    page_icon="👋",
)

# Create a page header

st.header("Videogame ESRB Prediction")

st.write("Hello! 👋")

st.write("This is a website made to showcase a model to predict the ESRB ratings of Video Games")






# Load the model you already created...
final_model = load_model()

# Begin user inputs




#read in the csv to get the features
cleaned_data = "data/final_model_data.csv"
df = pd.read_csv(cleaned_data)




st.subheader('Rating Predictor.')

st.write("Below you can enter the descriptors of a potential game and your input will be fed into the model and the prediction will be displayed")

st.write("If you want to see the prediction for a game without any descriptors just hit the predictor button")




#For the model input
selected_features = list(df.columns) #36
selected_features.remove("title") #35
selected_features.remove("esrb_rating") #34
selected_features.remove("esrb_encoded") #33
selected_features.remove("no_descriptors") #32


# For the dropdown list
descriptor_list = selected_features.copy()
descriptor_list.remove("num_descriptors") #31
descriptor_list.remove('ReleaseDate') #30

#allow user to select features 
user_descriptors = st.multiselect('Descriptors', descriptor_list)

#allow user to select a release date
date = st.text_input(label='When was the game released? YYYYMMDD')

# User runs prediction
clicked = st.button('Try out the Predictor?')



if (clicked) and re.compile("[1-2][0-9][0-9][0-9][0-1][0-9][0-3][0-9]").match(date):

    #create empty df
    row = {}
    for i in range(len(selected_features)):
        row[selected_features[i]] = [0]
    new_game_df = pd.DataFrame(row) #32

    #add the two non-listed features
    new_game_df.loc[0,"ReleaseDate"] = int(date)
    new_game_df.loc[0,"num_descriptors"] = len(clicked)

    #add the listed features
    for descriptor in descriptor_list:
        new_game_df.loc[0,descriptor] =1
    
    
    

    y_pred = final_model.predict(new_game_df)
    
    st.write("The model predicted that your game will be")

    if(y_pred == "E"):
        st.image('images/e_rating.png', width=50)

    elif(y_pred == "ET"):
        st.image('images/et_rating.png', width=50)

    elif(y_pred == "T"):
        st.image('images/t_rating.png', width=50)

    elif(y_pred == "M"):
        st.image('images/m_rating.png', width=50)

    else:
        st.write("Error")


    y_pred_proba = final_model.predict_proba(new_game_df)
    
    st.write("The probability for each of the categories in order of E, ET, M and T are")
    # maybe create the dataframe?

    ratings = ["E", "ET", "T", "M"]

    # changing the order

    list_prob = list(list(y_pred_proba[0]))

    # having some trouble with it saying I am out of range

    # needed to use the index of 0 from y_pred_proba

    probs = []

    for num in list_prob:
        probs.append(num*100)


    # swapping the T and M probablilities

    #st.write(probs)
    #st.write(probs[0])
    #st.write(probs[2])
    #st.write(probs[3])

    probs[2], probs[3] = probs[3], probs[2],



    paired_vals = list(zip(probs, ratings))

    #st.write(paired_vals)

    prob_df = pd.DataFrame(paired_vals, columns=["Probability", "ESRB Rating"])

    #st.write(probs)

    # maybe better and easier way to do this

    #st.dataframe(prob_df)

    #fig = px.bar( x=ratings, y=probs, title="Rating Probabilities", range_y= [0, 100])

    fig = px.bar(data_frame = prob_df, x="ESRB Rating", y="Probability", title="Rating Probabilities", range_y= [0, 100])

    # how to label the axis?

    # maybe make a dataframe?

    # also would be nice if there was an easy way to see when certain probabilities are very low

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })

    # changing the grid axes
    fig.update_xaxes(showgrid=False, gridwidth=1, gridcolor='Gray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Gray')

    # display graph
    st.plotly_chart(fig, use_container_width=True)

    # maybe there is a way to sort and to get rid of the key

    # also maybe sort by percent

    # or sort by proper rating order

    # would be nice to set Axes so it is always at max 100

  

    st.balloons()
