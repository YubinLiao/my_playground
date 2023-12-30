import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

# There are total of 43 type of traffic signs in the training data set
SIGN_NUMBER = 43
DATASET_PATH = "gtsrb"  # training data set path
images = []
labels = []

for i in range(SIGN_NUMBER):
    path = os.path.join(DATASET_PATH, str(i))
    for image in os.listdir(path):
        img = cv2.imread(os.path.join(DATASET_PATH, str(i), image))
        # resize all image to (30, 30), same as cnn input size
        img = cv2.resize(img, (30, 30))
        images.append(img)
        labels.append(i)

# labels has integer value between 0 and 42, convert to one-hot vector
# split to training and testing set with a ratio of 80:20
labels = tf.keras.utils.to_categorical(labels)
x_train, x_test, y_train, y_test = train_test_split(
    np.array(images), np.array(labels), test_size=0.2
)

# create a CNN model with 2 convolutional layer of 32 filters of 3x3 kernel
# and 2 Max-pooling of 2x2
# hidden layer of 256 nodes, with dropout
inputs = keras.Input(shape=(30, 30, 3))
x = layers.Conv2D(32, 3)(inputs)
x = layers.BatchNormalization()(x)
x = keras.activations.relu(x)
x = layers.MaxPooling2D()(x)
x = layers.Conv2D(64, 3)(x)
x = layers.BatchNormalization()(x)
x = keras.activations.relu(x)
x = layers.MaxPooling2D()(x)
x = layers.Flatten()(x)
x = layers.Dense(256, activation="relu")(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(SIGN_NUMBER, activation="softmax")(x)

model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

model.fit(x_train, y_train, epochs=10)

model.evaluate(x_test, y_test, verbose=2)

model.save("trained_model.keras")
