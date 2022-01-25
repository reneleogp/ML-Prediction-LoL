from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization

dataset = loadtxt('train_set.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:, 0:8]
y = dataset[:, 8]

print(X)

model = Sequential()


model.add(Dropout(0.69, input_dim=44))
model.add(BatchNormalization())
model.add(Dense(160, activation='elu', kernel_initializer='he_normal'))

model.add(Dropout(0.69))
model.add(BatchNormalization())
model.add(Dense(128, activation='elu', kernel_initializer='he_normal'))


model.add(Dropout(0.69))
model.add(BatchNormalization())
model.add(Dense(64, activation='elu', kernel_initializer='he_normal'))

model.add(Dropout(0.69))
model.add(BatchNormalization())
model.add(Dense(32, activation='elu', kernel_initializer='he_normal'))

model.add(Dropout(0.69))
model.add(BatchNormalization())
model.add(Dense(16, activation='elu', kernel_initializer='he_normal'))

model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['accuracy'])

model.fit(X, y, epochs=150, batch_size=10, verbose=0)

_, accuracy = model.evaluate(X, y, verbose=0)
print('Accuracy: %.2f' % (accuracy*100))
