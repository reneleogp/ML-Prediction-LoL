# Predicting the outcome of a League of Legends game based on Champion-Player Experience with 90% of accuracy

First of all, this project is heavily inspired on this [research](https://arxiv.org/abs/2108.02799#:~:text=Using%20a%20deep%20neural%20network,for%20playing%20LoL%20and%20matchmaking.). So shoutout to them.

## Preview

I implemented a serious of Machine Learning algorithms to determinate the outcome of a League of Legends game based on Player-Champion Experience. I used more than 15k matches from two different servers, in order to make the training and predictions. My best result was 91% of accuracy using GBOOST.

## Introduction

League of Legends (LoL), a popular computer game developed by Riot Games, is currently the most widely played Multiplayer Online Battle Arena (MOBA) game in the world. In 2019, there were eight million concurrent players daily, and the player base has continued to grow since its release in 2009. A core aspect of LoL is competitive ranked gameplay. In typical ranked gameplay, ten human players are matched together to form two teams of approximately equal skill. These two teams, consisting of five players each, battle against each other to destroy the opposing team’s base.

To the matchmaker, a “fair” match can be loosely defined as a match in which each team has a 50% +/-1% chance of winning. In a perfect match, ten individuals with identical MMRs queue at the same time, each having selected a unique position that they’re well-suited for. That situation is incredibly rare depending on who is queueing at the time, so sometimes teams can have very slight skill differences.

Even though Riot has been trying to make the matchmaking as fair as poosible the fact that LoL has 150 characters with different abilities and positions can heavily impact on a match. For instance if player plays a champion who hasn't played before against someone with a close skill this person is more likely to lose.

Based on these final preposition I decided to create an machine learning algorithm to predict the outcome of a League of Legends game based on Player-Champion Experience

## Datasets

The most important part of your algorithm are your dataset. So I needed a good amount of matches(samples) to train my algorithm. These are the steps I followed:

1. First I got around 875 random summoners from each ranking from Iron to Diamond using Riot's API 
2. Using these summoners I got their last 3 Solo-Ranked matches from Mobalytics API. Making a total of 14k games
3. Then I got the masteries from [championmastery.gg](https://championmastery.gg/)
4. Then I got the winrates of season 11 and 12 from [u.gg](https://u.gg/)
5. Finally I saved everything in my mongodb database and saved to train the algorithm
   
## Models

- I used two models a GBOOST and a Deep neural network being the Gradient boosting the best with an accuracy up to 91%




