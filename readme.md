# Predicting the outcome of a League of Legends game based on Champion-Player Experience

First of all, this project is heavily inspired on this [research](https://arxiv.org/abs/2108.02799#:~:text=Using%20a%20deep%20neural%20network,for%20playing%20LoL%20and%20matchmaking.). So shoutout to them.

## Preview

I implemented a two Machine Learning algorithms to determinate the outcome of a League of Legends game based on Player-Champion Experience. I used more than 16k matches from two different servers, in order to make the training and predictions. My best result was 91% of accuracy using GBOOST.

## Introduction

League of Legends (LoL), a popular computer game developed by Riot Games, is currently the most widely played Multiplayer Online Battle Arena (MOBA) game in the world. In 2019, there were eight million concurrent players daily, and the player base has continued to grow since its release in 2009. A core aspect of LoL is competitive ranked gameplay. In typical ranked gameplay, ten human players are matched together to form two teams of approximately equal skill. These two teams, consisting of five players each, battle against each other to destroy the opposing team’s base.

To the matchmaker, a “fair” match can be loosely defined as a match in which each team has a 50% +/-1% chance of winning. In a perfect match, ten individuals with identical MMRs queue at the same time, each having selected a unique position that they’re well-suited for. That situation is incredibly rare depending on who is queueing at the time, so sometimes teams can have very slight skill differences.

Even though Riot has been trying to make the matchmaking as fair as poosible the fact that LoL has 150 characters with different abilities and positions can heavily impact on a match. For instance if player plays a champion who hasn't played before against someone with a close skill this person is more likely to lose.

Based on these final preposition I decided to create an machine learning algorithm to predict the outcome of a League of Legends game based on Player-Champion Experience.

## Datasets

The most important part of your algorithm are your dataset. So I needed a good amount of matches(samples) to train my algorithm. These are the steps I followed:

From LAN server:

1. First I got around 875 random summoners from each ranking from Iron to Diamond using Riot's API. Making a total of 5250 summoners.
2. Using these summoners I got their last 3 Solo-Ranked matches from [Mobalytics](https://mobalytics.gg/) API. Using the match ID I disregarded repeated matches. Making a total of 14k unique matches.

From NA server:
1. Did the same thing to get the summoners
2. Did the same thing to get the past games but in this case I only got their last SoloQ match.
   
**For each player in each match I got:**
   
1. Their champion-masteries from [championmastery.gg](https://championmastery.gg/) via web scraping.
2. Their winrates with each champion in SoloQ games of season 11 and 12 (a combination of both seasons). From [u.gg](https://u.gg/) API. (A number from 0 to 1).

Finally I saved everything in my mongodb database to later process the data and train the algorithm.

**This made a total of 12458 unique SoloQ games from LAN server and 4552 SoloQ matches from NA server.**

The functions to get the save the data can be found in the file [pull_data_scripts.py](https://github.com/PlayErphil/ML-Prediction-LoL/blob/master/src/get_data_training/pull_data_scripts.py). While the functions to call the APIs can be found in the file [api_calls.py](https://github.com/PlayErphil/ML-Prediction-LoL/blob/master/src/api_calls/api_calls.py)

## Processing the data

I processed the data in the format to pass it into the algorithm.

For both teams in each math I added the following features:

1. Mastery of each summoner with their selected champion. (5 features per team).
2. Average, median, coefficient of kurtosis, coefficient of skewness, standard deviation, and variance of the masteries of the team. (6 features per team).
3. Winrate of each summoner with their selected champion. (5 features per team).
4. Average, median, coefficient of kurtosis, coefficient of skewness, standard deviation, and variance of the winrates of the team. (6 features per team).

Making a total of 22 features per team or, 44 features per match.

Finally at the end of the sample we add the label (output). 1 if the blue team won or 0 otherwise.

Here is an example of the some finished samples:

| Blue Mastery 1 | Blue Mastery 2 | Blue Mastery 3 | Blue Mastery 4 | Blue Mastery 5 | Blue Masteries Avg | Blue Masteries Median | Blue Masteries Kurtorsis | Blue Masteries Skewness | Blue Masteries Std | Blue Masteries Variance | Blue Winrate 1      | Blue Winrate 2     | Blue Winrate 3      | Blue Winrate 4      | Blue Winrate 5      | Blue Winrates Avg   | Blue Winrates Median | Blue Winrates Kurtorsis | Blue Winrates Skewness | Blue Winrates Std    | Blue Winrates Variance | Red Mastery 1 | Red Mastery 2 | Red Mastery 3 | Red Mastery 4 | Red Mastery 5 | Red Masteries Avg | Red Masteries Median | Red Masteries Kurtorsis | Red Masteries Skewness | Red Masteries Std  | Red Masteries Variance | Red Winrate 1      | Red Winrate 2      | Red Winrate 3       | Red Winrate 4       | Red Winrate 5      | Red Winrates Avg    | Red Winrates Median | Red Winrates Kurtorsis | Red Winrates Skewness | Red Winrates Std    | Red Winrates Variance | Blue Won |
| -------------- | -------------- | -------------- | -------------- | -------------- | ------------------ | --------------------- | ------------------------ | ----------------------- | ------------------ | ----------------------- | ------------------- | ------------------ | ------------------- | ------------------- | ------------------- | ------------------- | -------------------- | ----------------------- | ---------------------- | -------------------- | ---------------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ----------------- | -------------------- | ----------------------- | ---------------------- | ------------------ | ---------------------- | ------------------ | ------------------ | ------------------- | ------------------- | ------------------ | ------------------- | ------------------- | ---------------------- | --------------------- | ------------------- | --------------------- | -------- |
| 302361         | 32548          | 137831         | 42344          | 2594552        | 621927.2           | 137831.0              | 4.804286377468026        | 2.1839427059899292      | 991060.5244612258  | 982200963145.36         | 0.44642857142857145 | 0.5882352941176471 | 0.23076923076923075 | 0.42857142857142855 | 0.5064102564102564  | 0.4400829562594269  | 0.44642857142857145  | 1.7867390843738296      | -1.0057794278406758    | 0.11860307225221957  | 0.014066688747665215   | 161323        | 69486         | 860782        | 5651          | 760456        | 371539.6          | 161323.0             | -3.0230679355840793     | 0.5602290310596598     | 363294.90939048404 | 131983191189.04        | 0.5522388059701493 | 0.6                | 0.4857142857142857  | 0.33333333333333326 | 0.5883838383838383 | 0.5119340526803213  | 0.5522388059701493  | 1.7550266381659405     | -1.4411615960973314   | 0.09778583443443616 | 0.00956206941603896   | 0        |
| 244724         | 55894          | 166393         | 151398         | 17928          | 127267.4           | 151398.0              | -1.3369649217205293      | 0.01316455063445954     | 81189.18392889536  | 6591683587.040001       | 0.5454545454545454  | 0.625              | 0.39893617021276595 | 0.5                 | 0.0                 | 0.4138781431334623  | 0.5                  | 2.9264103385945406      | -1.6520677083219906    | 0.21946304574713268  | 0.04816402844860805    | 33130         | 9301          | 415872        | 82639         | 15557         | 111299.8          | 33130.0              | 4.422881427922964       | 2.08903337480402       | 154445.2155651317  | 23853324610.96         | 0.7142857142857143 | 0.5384615384615384 | 0.5511363636363636  | 0.6415094339622641  | 0.5                | 0.5890786100691761  | 0.5511363636363636  | -0.9509293445462141    | 0.7660317416649389    | 0.07792626131767952 | 0.006072502202951276  | 0        |
| 1370461        | 165699         | 328554         | 11922          | 64623          | 388251.8           | 165699.0              | 4.0663657209767          | 1.9913240765628601      | 502829.6346149061  | 252837641446.95996      | 0.5311284046692607  | 0.543859649122807  | 0.4878048780487805  | 0.4444444444444444  | 0.43333333333333335 | 0.48811414192372526 | 0.4878048780487805   | -2.714615983530692      | 0.01750089360642681    | 0.044420408562547566 | 0.0019731726968636493  | 24674         | 69412         | 24297         | 197578        | 1344271       | 332046.4          | 69412.0              | 4.679175538952802       | 2.153192672198477      | 510067.58473543485 | 260168940997.84        | 0.7333333333333333 | 0.4705882352941176 | 0.631578947368421   | 0.5357142857142857  | 0.5294117647058824 | 0.5801253132832079  | 0.5357142857142857  | -0.1714387569448257    | 0.8322535703305709    | 0.09237180165145097 | 0.008532549740335     | 0        |
| 859153         | 8207           | 152833         | 30736          | 94462          | 229078.2           | 94462.0               | 4.494974145065102        | 2.0987197424240636      | 319077.67728589225 | 101810564142.16         | 0.594               | 0.5833333333333334 | 0.5833333333333334  | 0.5                 | 0.6111111111111112  | 0.5743555555555556  | 0.5833333333333334   | 3.8040034295105913      | -1.835360837059765     | 0.03854043251277294  | 0.0014853649382716057  | 7376          | 19807         | 249551        | 1914694       | 2021545       | 842594.6          | 249551.0             | -3.24972252904008       | 0.5761330822350282     | 923644.0250595681  | 853118285028.24        | 0.0                | 0.5                | 0.14285714285714285 | 0.5157894736842106  | 0.5236318407960199 | 0.33645569146747467 | 0.5                 | -2.252574646473776     | -0.7891605499808829   | 0.22119000317369086 | 0.048925017503977375  | 1        |

   
The function for processing the data can be found in the file [process_data.py](https://github.com/PlayErphil/ML-Prediction-LoL/blob/master/src/get_data_training/process_data.py). Note that this is processing matches with the data gathered from the APIs that is stored in my Mongo database.

## Models

### Deep Neural Network

The model architecture uses keras and following the structure as described in the research paper:

• Alternating dropout, normalization, and dense layers for a total of 15 layers (5 dropout, 5 normalization, and 5 dense
layers). Each group of alternating layers had 160, 128, 64, 32, and 16 neurons, in that order.

- Each dropout layer had a dropout rate of 0.69%.
- Each normalization layer utilized batch normalization.
- Each dense layer used Exponential Linear Unit (ELU) activation, He initialization.
- A 1 × 1 dense layer with Sigmoid activation

Then we fit our model using the following parameters `epochs=49` and `batch_size=256`. 

**Note that we use the LAN matches for training and the NA matches for testing and validation.**

Finally we evauluate the model with the train samples and validation samples. In this case we use the LAN matches for training and NA matches for testing.

The jupiter notebook can be found [here](https://github.com/PlayErphil/ML-Prediction-LoL/blob/master/src/neural_network.ipynb)


### Gradient Boosting

- The model is written using the sklearn implementation of GBOOST, which by default is a Decision Tree, with the following parameters: `n_estimators=55` and `learning_rate=0.14`
  
  **NOTE: I used a Stratified K Fold to test the algorithm in order to get a more accurate result, with `k=10`.** 

The jupiter notebook can be found [here](https://github.com/PlayErphil/ML-Prediction-LoL/blob/master/src/gboost.ipynb)

## Results

The DNN model performed better than expected with an **accuracy of 82%** in the testing dataset (more than 4552 matches). 

In the other hand the GBOOST showed an **average accuracy of 89.42%!!!**, a minimum of 88.48% and a **maximum of 90.48%**. 

## Future work

In future work I would like to add the role experience as a feature.

# Try the finalized Algorithm!

I did a simple UI using streamlit under the src/app.py you can run it by installing streamlit package and with the command `streamlit run "your_path_to_app.py"`. I get the last match from [u.gg](https://u.gg/) API.






