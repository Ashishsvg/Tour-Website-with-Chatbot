from flask import Flask, send_from_directory, request, jsonify
import csv
import os
import random
import re

app = Flask(__name__)

# Load CSV data
csv_data = []
csv_file_path = 'static/travel_places_weather.csv'

if os.path.exists(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        csv_data = list(reader)

# Synonym map
synonym_map = {
    "hi": ["hello", "hey", "yo", "hiya"],
    "how are you": ["how is life", "how are you doing", "how's it going"],
    "suggest a destination": ["where should I travel", "best places to visit", "places to go", "top destinations", "recommend a place"],
    "travel documents": ["what documents are needed", "what documents for travel", "passport", "visa", "travel papers"],
    "book flights": ["how to book flights", "how to find cheap flights", "flight booking tips", "how to book cheap flights"],
    "hotel suggestions": ["where can I stay", "suggest hotels", "where to stay", "place to sleep"],
    "things to pack": ["packing tips", "what should I carry", "travel packing list", "things to carry"],
    "travel insurance": ["is insurance needed", "insurance for trips", "should I get insurance"],
    "help me": ["tell me about travel", "travel tips", "travel help"],
    "thank you": ["thanks", "appreciate it"],
    "i love you": ["love you", "i like you"],
    "bye": ["goodbye", "see you", "later"]
}

user_message = list(synonym_map.keys())

bot_reply = [
    ["Hello there! Ready to plan your next trip?"],
    ["Doing great! Planning your next adventure?"],
    ["How about France, Switzerland, or Japan?"],
    ["You'll need your passport, visa (if required), and travel insurance."],
    ["Use Skyscanner, Google Flights, or Kayak to book affordable flights."],
    ["Try Booking.com or Airbnb for comfy places to stay!"],
    ["Ask me about a country, and I’ll share the weather info!"],
    ["Pack light, bring layers, and don't forget your charger and passport!"],
    ["Insurance can really help in emergencies. I'd recommend getting one!"],
    ["Sure! Ask me anything about travel, destinations, or packing!"],
    ["You're welcome!"],
    ["I love travel buddies too!"],
    ["Safe travels! Hope to chat again soon."]
]

alternative = [
    "Can you ask me something related to travel?",
    "That's interesting! Let's talk about your next trip.",
    "Need help packing or picking a place?",
    "Hmm, I'm best at travel advice. Want suggestions?"
]

# Normalize and match input with synonyms
def normalize_message(msg):
    msg = re.sub(r'[^\w\s]', '', msg.lower())  # remove punctuation
    for keyword, synonyms in synonym_map.items():
        if keyword in msg:
            return keyword
        for syn in synonyms:
            if syn in msg:
                return keyword
    return msg

# Match message to response
def compare_message(user_input):
    normalized = normalize_message(user_input)
    if normalized in user_message:
        index = user_message.index(normalized)
        return random.choice(bot_reply[index])
    return None

# Check for country-specific queries from CSV
def check_weather_or_places(msg):
    msg = msg.lower()
    for entry in csv_data:
        country = entry["Country"].lower()
        if "weather" in msg and country in msg:
            return f"Typical weather in {entry['Country']}: {entry['Typical Weather']}"
        if country in msg:
            return f"Some amazing places to visit in {entry['Country']}: {entry['Popular Places']}"
    return None

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = compare_message(user_input)
    if not response:
        response = check_weather_or_places(user_input)
    if not response:
        response = random.choice(alternative)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
