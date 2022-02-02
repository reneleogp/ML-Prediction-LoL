from tkinter.messagebox import NO
import streamlit as st
import numpy as np
import pandas as pd
from predict import get_current_match_prediction, get_last_match_prediction

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()
predict_current_match = st.container()
predict_last_match = st.container()


last_summoner_name = "a"

with header:
    st.title("Welcome to my awsome project!")
    st.text("This project predicts a League of Legends outcome")

with dataset:
    st.header("12k Unique matches")
    st.text(
        "I trained my algorithm with 12k unique matches matches from LAN server from ranked games, all ranging from Iron to Diamond, divided evenly"
    )

with features:
    st.header("Features: ")
    st.subheader("I used 44 features per match:")

    st.markdown(
        "1. The winrates of each summoner with their champion in season 11 and 12, making a total of 10 features"
    )
    st.markdown(
        "2. The masteries of each summoner with their champion, making a total of 10 features"
    )
    st.markdown(
        "3. From each team masteries and winrates list (4 lists) I got: mean, average, coeficient of kurtosis, skewness, standard deviation and variance"
    )

    st.markdown(
        "Making a total of 44 features, and at the end we can see if the blue team won or not"
    )

    match_data = pd.read_csv("na_dataset.csv")
    st.write(match_data.head())


with model_training:
    st.header("I used a GBOOST and a Deep neural network")

with predict_current_match:
    st.header("Predict Current Match!")

    sel_col, disp_col = st.columns(2)
    summoner_name = sel_col.text_input("What is your Summoner Name?", "kokkurit")
    region = sel_col.selectbox(
        "What is your Region?",
        options=[
            "LAN",
            "NA",
            "LAN",
            "LAS",
            "NA",
            "EUW",
            "EUNE",
            "BR",
            "JP",
            "KR",
            "OCE",
            "RU",
            "TR",
        ],
    )

    if summoner_name != last_summoner_name:
        data = get_current_match_prediction(summoner_name, region)
        last_summoner_name = summoner_name

    print(data)
    if data == None:
        disp_col.subheader("No current game")
    else:
        disp_col.subheader(f"Your team is:")
        disp_col.write(data["team"])

        disp_col.subheader(f"Your role is:")
        disp_col.write(data["role"])

        disp_col.subheader(f"Your champion is:")
        disp_col.write(data["champion"])

        disp_col.subheader(f"Our prediction is:")
        if data["victory_predicted"]:
            disp_col.write("Victory!")
        else:
            disp_col.write("Defeat :(")


with predict_last_match:
    st.header("Predict last match!")

    sel_col, disp_col = st.columns(2)
    summoner_name = sel_col.text_input("What is your Summoner Name?", "pentaculos3k")
    region = sel_col.selectbox(
        "What is your Region????",
        options=[
            "LAN",
            "NA",
            "LAN",
            "LAS",
            "NA",
            "EUW",
            "EUNE",
            "BR",
            "JP",
            "KR",
            "RU",
            "TR",
        ],
    )

    if summoner_name != last_summoner_name:
        data = get_last_match_prediction(summoner_name, region)
        last_summoner_name = summoner_name

    print(data)
    disp_col.subheader(f"Your team was:")
    disp_col.write(data["team"])

    disp_col.subheader(f"Your role was:")
    disp_col.write(data["role"])

    disp_col.subheader(f"Your champion was:")
    disp_col.write(data["champion"])

    disp_col.subheader(f"Your game result was:")

    if data["won"]:
        disp_col.write("Victory")
    else:
        disp_col.write("Lost")

    disp_col.subheader(f"Our prediction was:")
    if data["correct"]:
        disp_col.write("Correct!")
    else:
        disp_col.write("Incorrect :(")
