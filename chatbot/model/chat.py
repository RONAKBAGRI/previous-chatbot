from flask import Flask, request, jsonify
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from flask_cors import CORS  # To allow frontend to access backend

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")  # Enable CORS to allow requests from your React Native app

# Load chatbot data
with open('C:\\Users\\Ronak Bagri\\Downloads\\Chatbot\\chatbot\\model\\final_merged_data.json', 'r', encoding="utf-8") as json_data:
    intents = json.load(json_data)

FILE = "C:\\Users\\Ronak Bagri\\Downloads\\Chatbot\\chatbot\\model\\final.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

bot_name = "Svaran"

def get_response(msg):
    sentence = str(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).float()

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "I do not understand..."

# Create an API endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    print(f"Received message: {data.get('message')}")
    user_message = data.get("message")
    bot_reply = get_response(user_message)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
