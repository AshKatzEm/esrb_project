import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px



st.set_page_config(
    page_title="ESRB Prediction",
    page_icon="👋",
)

# Create a page header

st.header("Videogame ESRB Prediction")

st.write("Hello! 👋")

st.write("This is a website made to showcase a model to predict the ESRB ratings of Video Games")






# Load the model you already created...
final_model = pickle.load(open('esrb_project/models/final_model.pkl', 'rb'))

# needed to save the model my own way instead of how the boilerplate way

# tried downloading another attempt to save

# Begin user inputs





# since we now split up the model

# and the cleaning I have to read in the csv to get the features

# should I read from local repo or from github?


cleaned_data = "https://raw.githubusercontent.com/HA-work/esrb_project/main/data/cleaned_games.csv"


df = pd.read_csv(cleaned_data)




st.subheader('Rating Predictor.')

st.write("Below you can enter the descriptors of a potential game and your input will be fed into the model and the prediction will be displayed")

st.write("If you want to see the prediction for a game without any descriptors just hit the predictor button")





selected_features = list(df.columns)



selected_features.remove("title")
selected_features.remove("esrb_encoded")
selected_features.remove("esrb_rating")
selected_features.remove("no_descriptors")


descriptor_list = selected_features.copy()



descriptor_list.remove("num_descriptors")


user_descriptors = st.multiselect('Descriptors', descriptor_list)


clicked = st.button('Try out the Predictor?')

old = list()
while old != user_descriptors:
    count = len(user_descriptors) 
    new_game_values = [] 
    for descriptor in descriptor_list: 
        if (descriptor in user_descriptors):
            new_game_values.append(1) 
        else: 
            new_game_values.append(0) 


    viz_game_df = pd.DataFrame([new_game_values], columns = descriptor_list)
    new_game_values.append(count)
    new_game_df = pd.DataFrame([new_game_values], columns = selected_features )

    old = user_descriptors
    mask = pd.Series(data=0, index= range(len(df)))
    for i in descriptor_list:
        if int(viz_game_df[i]):
            for j in (df[i] == 1).index:
                mask[j] += int((df[i] == 1)[j])
    
    for i in mask.index:
        if mask[i] == len(user_descriptors):
            mask[i] = True
        else:
            mask[i] = False
    if len(df[mask]) > 0:        
        fig = px.pie(df[mask],
                     values=df['esrb_rating'][mask].value_counts(),
                     names = df['esrb_rating'][mask].value_counts().index,
                     title='ESRB ratings'
                    )
        st.plotly_chart(fig, sharing="streamlit")
    else:
        st.error('No games fit that description', icon = '😿')
    

 
    
    
    
    
    
    
    
    
if (clicked):
    # count = len(user_descriptors)
    # new_game_values = []
    # for descriptor in descriptor_list:
    #     if (descriptor in user_descriptors):
    #         new_game_values.append(1)
    #     else:
    #         new_game_values.append(0)
    # new_game_values.append(count)
    # new_game_df = pd.DataFrame([new_game_values], columns=selected_features)

 

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

    #st.write(y_pred)

    y_pred_proba = final_model.predict_proba(new_game_df)
    
    st.write("The probability for each of the categories in order of E, ET, M and T are")

    #st.write(y_pred_proba)

    # what if a prediction is 50-50


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






