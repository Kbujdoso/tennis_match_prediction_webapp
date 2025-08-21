import tensorflow as tf
from keras.models import Model
from keras.layers import LSTM, Dense, Input, Concatenate, Masking, Dropout
import numpy as np
from normalizer_for_lstm import data_set_creator_lstm
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
import collections


print("Label distribution:")
MASK_VALUE = -1.0

data_set = data_set_creator_lstm("matches.csv")
data, label = zip(*data_set)
player_features, player_history_1, player_history_2 = zip(*data)

x_features = np.array(player_features)
x_history_1 = np.array(player_history_1)
x_history_2 = np.array(player_history_2)
y = np.array(label)

print(collections.Counter(y))

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_features_scaled = scaler.fit_transform(x_features)

def scale_with_mask(data, mask_value):
    mask = (data == mask_value)
    data_nan = np.where(mask, np.nan, data)
    reshaped = data_nan.reshape(-1, data.shape[-1])
    mean = np.nanmean(reshaped, axis=0)
    std = np.nanstd(reshaped, axis=0)
    scaled = (reshaped - mean) / std
    scaled[mask.reshape(-1, data.shape[-1])] = mask_value
    return scaled.reshape(data.shape)

x_history_1_scaled = scale_with_mask(x_history_1, MASK_VALUE)
x_history_2_scaled = scale_with_mask(x_history_2, MASK_VALUE)

x_scaled = list(zip(x_features_scaled, x_history_1_scaled, x_history_2_scaled))
combined = list(zip(x_scaled, y))
np.random.seed(42)
np.random.shuffle(combined)

x, y = zip(*combined)
y = np.array(y)
player_features, player_history_1, player_history_2 = zip(*x)
x_features = np.array(player_features)
x_history_1 = np.array(player_history_1)
x_history_2 = np.array(player_history_2)

x_features_train, x_features_temp, \
x_history_1_train, x_history_1_temp, \
x_history_2_train, x_history_2_temp, \
y_train, y_temp = train_test_split(
    x_features, x_history_1, x_history_2, y,
    test_size=0.4, random_state=42
)

x_features_val, x_features_test, \
x_history_1_val, x_history_1_test, \
x_history_2_val, x_history_2_test, \
y_val, y_test = train_test_split(
    x_features_temp, x_history_1_temp, x_history_2_temp, y_temp,
    test_size=0.5, random_state=42
)

print(x_features_train.shape)
print(x_history_1_train.shape)
print(x_history_2_train.shape)

input_features = Input(shape=(x_features.shape[1],))
input_history_1 = Input(shape=(30, 51))
input_history_2 = Input(shape=(30, 51))

masked_history_1 = Masking(mask_value=MASK_VALUE)(input_history_1)
masked_history_2 = Masking(mask_value=MASK_VALUE)(input_history_2)

lstm1 = LSTM(256, return_sequences=True)(masked_history_1)
lstm1 = LSTM(128)(lstm1)

lstm2 = LSTM(256, return_sequences=True)(masked_history_2)
lstm2 = LSTM(128)(lstm2)

concat = Concatenate()([input_features, lstm1, lstm2])
dense = Dense(512, activation='relu')(concat)
dense = Dropout(0.3)(dense)
hidden = Dense(256, activation='relu')(dense)
hidden = Dropout(0.3)(hidden)
hidden2 = Dense(64, activation='relu')(hidden)
hidden2 = Dropout(0.3)(hidden2)
output = Dense(1, activation='sigmoid')(hidden2)

model = Model(inputs=[input_features, input_history_1, input_history_2], outputs=output)
loss = tf.keras.losses.BinaryCrossentropy(label_smoothing=0.1)
model.compile(optimizer='adam', loss=loss, metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)


model.fit(
    [x_features_train, x_history_1_train, x_history_2_train],
    y_train,
    validation_data=([x_features_val, x_history_1_val, x_history_2_val], y_val),
    epochs=15,
    callbacks=[early_stopping]
)

test_loss, test_acc = model.evaluate([x_features_test, x_history_1_test, x_history_2_test], y_test)
print(f"Test accuracy: {test_acc:.4f}")

model.summary()
model.save('tennis_betting_first_release.keras')
