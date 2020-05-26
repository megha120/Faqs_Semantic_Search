#Importing the required libraries
import os
import search as search
from flask_cors import CORS
from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, Api


#Setting up the Flask app
app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}}) 


#Defining the template 
@app.route('/')
def index():
    return render_template('index.html')


#Method to invoke the search accepting the query string as a parameter
@app.route('/search')
def analyzer():
    query = request.args.get('q')
    response = search.logic(query)
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
