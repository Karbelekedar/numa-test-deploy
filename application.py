from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS


application = app = Flask(__name__)
CORS(application)

application.config["MONGO_URI"] = "mongodb+srv://echo:PjRboQ0F7xcMvPMI@cluster0.7ij7o2z.mongodb.net/Echo?retryWrites=true&w=majority"
mongo = PyMongo(application)

@application.route('/')
def home():
    return """
    <html>
        <head>
            <title>Home Page</title>
        </head>
        <body>
            <h1>Welcome to our website!</h1>
        </body>
    </html>
    """

@application.route('/register', methods=['POST'])
def register():
    data = request.json
    if data and 'email' in data and 'password' in data:
        hashed_password = generate_password_hash(data['password'])
        mongo.db.users.insert_one({'email': data['email'], 'password': hashed_password})
        return jsonify({'message': 'User registered successfully', 'email': data['email']}), 201
    else:
        return jsonify({'message': 'Invalid data'}), 400
    

@application.route('/login', methods=['POST'])
def login():
    data = request.json
    if data and 'email' in data and 'password' in data:
        user = mongo.db.users.find_one({'email': data['email']})
        if user and check_password_hash(user['password'], data['password']):
            return jsonify({'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
    else:
        return jsonify({'message': 'Invalid data'}), 400
    

@application.route('/details', methods=['POST'])
def details():
    data = request.json
    if data and 'name' in data and 'dob' in data and 'email' in data:
        user = mongo.db.users.find_one({'email': data['email']})
        if user:
            mongo.db.users.update_one({'email': data['email']}, {'$set': {'name': data['name'], 'dob': data['dob']}})
            return jsonify({'message': 'Details updated successfully'}), 200
        else:   
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Invalid data'}), 400
    



if __name__ == '__main__':
    application.run(debug=True)