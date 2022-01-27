import streamlit as st
import numpy as np
import pandas as pd
from predict import predict_last_match

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()
prediciton = st.container()

last_summoner_name = 'a'

with header:
    st.title('Welcome to my awsome project!')
    st.text('This project predicts a League of Legends outcome')

with dataset:
    st.header('12k Unique matches')
    st.text('I trained my algorithm with 12k unique matches matches from LAN server from ranked games, all ranging from Iron to Diamond, divided evenly')

with features:
    st.header('Features: ')
    st.subheader('I used 44 features per match:')

    st.markdown(
        '1. The winrates of each summoner with their champion in season 11 and 12, making a total of 10 features')
    st.markdown(
        '2. The masteries of each summoner with their champion, making a total of 10 features')
    st.markdown('3. From each team masteries and winrates list (4 lists) I got: mean, average, coeficient of kurtosis, skewness, standard deviation and variance')

    st.markdown(
        'Making a total of 44 features, and at the end we can see if the blue team won or not')

    match_data = pd.read_csv('na_dataset.csv')
    st.write(match_data.head())


with model_training:
    st.header('I used a GBOOST and a Deep neural network')

with prediciton:
    st.header('Now lets make a prediciton on your last game!')

    sel_col, disp_col = st.columns(2)
    summoner_name = sel_col.text_input(
        'What is your Summoner Name?', 'pentaculos3k')
    region = sel_col.text_input(
        'What is your Region?', 'LAN')

    print(summoner_name)
    print(last_summoner_name)
    if(summoner_name != last_summoner_name):
        data = predict_last_match(summoner_name, region)
        last_summoner_name = summoner_name

    disp_col.subheader(f'Your team was:')
    disp_col.write(data['team'])

    disp_col.subheader(f'Your role was:')
    disp_col.write(data['role'])

    disp_col.subheader(f'Your champion was:')
    disp_col.write(data['champion'])

    disp_col.subheader(f'Your game result was:')

    if(data['won']):
        disp_col.write('Victory')
    else:
        disp_col.write('Lost')

    disp_col.subheader(f'Our prediction was:')
    if(data['correct']):
        disp_col.write('Correct!')
    else:
        disp_col.write('Incorrect :(')
