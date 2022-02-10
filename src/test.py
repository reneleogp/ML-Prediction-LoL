import pandas as pd
import numpy as np

lan_df = pd.read_csv("/Users/renegonzalez/Desktop/DNN LoL/lan_dataset.csv")
na_df = pd.read_csv("/Users/renegonzalez/Desktop/DNN LoL/na_dataset.csv")
lan_df.head()

frames = [lan_df, na_df]

result = pd.concat(frames)

# Convert the entire DataFrame
dataset = result.to_numpy()

np.random.shuffle(dataset)

X = dataset[:, 0:44]
Y = dataset[:, 44]

X.shape, Y.shape

from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier(n_estimators=55, learning_rate=0.14)
