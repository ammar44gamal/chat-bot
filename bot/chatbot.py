import json
import random
import pickle
import numpy as np
from tensorflow.keras.models import load_model # type: ignore

# Load intents
with open("bot/intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

# Load trained model, vectorizer, and label encoder
model = load_model("bot/uneeqbot_model.h5")
with open("bot/label_encoder.pkl", "rb") as f:
    lbl_enc = pickle.load(f)
with open("bot/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Function to get AI response
def get_response(user_input):
    # Transform input using TF-IDF vectorizer
    user_vec = vectorizer.transform([user_input]).toarray()
    
    # Predict intent
    pred_idx = np.argmax(model.predict(user_vec, verbose=0), axis=-1)[0]
    tag = lbl_enc.inverse_transform([pred_idx])[0]
    
    # Return a random response from the matched intent
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

# Console testing
if __name__ == "__main__":
    print("UneeqBot 🤖 is running! Type 'quit' to exit.")
    while True:
        msg = input("You: ")
        if msg.lower() == "quit":
            break
        print("UneeqBot 🤖:", get_response(msg))