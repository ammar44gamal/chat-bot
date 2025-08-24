import json
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

# -------------------
# Step 1: Load intents and preprocess
# -------------------
with open('bot/intents.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

patterns = []
labels = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        labels.append(intent['tag'])

lbl_enc = LabelEncoder()
y = lbl_enc.fit_transform(labels)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns).toarray()

print("Patterns shape:", X.shape)
print("Labels shape:", y.shape)

# -------------------
# Step 2: Build and train the model
# -------------------
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense # type: ignore
import pickle

model = Sequential()
model.add(Dense(128, input_shape=(X.shape[1],), activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(lbl_enc.classes_), activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X, y, epochs=200, batch_size=8, verbose=1)

# Save the model and preprocessing objects
model.save('bot/uneeqbot_model.h5')

with open('bot/label_encoder.pkl', 'wb') as f:
    pickle.dump(lbl_enc, f)

with open('bot/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model training complete and saved!")