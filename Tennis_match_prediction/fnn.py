import os 
import pandas as pd 
from datetime import datetime 
from normalize import data_set_creator
import json
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split



"""train_data, test_data = data_set_creator("matches_test.csv")
print(len(train_data))
print(len(test_data))"""
data_set = data_set_creator("matches.csv")
"""x_train, y_train = zip(*train_data)
x_test, y_test = zip(*test_data)"""

x_raw, y_raw = zip(*data_set)
x_raw = np.array(x_raw)
y_raw = np.array(y_raw)


scaler = StandardScaler()
x_scaled = scaler.fit_transform(x_raw)

combined = list(zip(x_scaled, y_raw))
np.random.seed(42)
np.random.shuffle(combined)

x, y = zip(*combined)
x = np.array(x)
y = np.array(y)

x_train, x_temp, y_train, y_temp = train_test_split(
    x, y, test_size=0.4, random_state=42
)
x_val, x_test, y_val, y_test = train_test_split(
    x_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)

 

train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(100).batch(16)
test_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(16)
val_dataset = tf.data.Dataset.from_tensor_slices((x_val, y_val)).batch(16)


model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(1913,)),
    tf.keras.layers.Dense(512, activation="relu"),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(256, activation="relu"),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])



model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=tf.keras.losses.BinaryCrossentropy(),
    metrics=[tf.keras.metrics.BinaryAccuracy()]
    )

model.fit(
    train_dataset,
    epochs = 8,
    validation_data = val_dataset,
)

test_loss, test_acc = model.evaluate(test_dataset)
print(f"Test accuracy: {test_acc:.4f}")
