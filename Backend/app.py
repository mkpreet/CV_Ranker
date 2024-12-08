from flask import Flask, request, jsonify
from flask_cors import CORS
import cv_match 

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def home():
    return "Hello World, from Flask!"

@app.route("/postdata", methods=["POST"])
def post_data():
    # Get the JSON data from the request
    data = request.get_json()
    print("Received data:", data)
    
    scores=cv_match.print_score(data)
    # Return the received data as a response
    #return scores
    return jsonify(scores), 200
    # return data
