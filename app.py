from flask import Flask, request, jsonify
from database.user_model import Users
from config import db
import os

app = Flask(__name__)

# Set up database path
db_path = os.path.join(os.getcwd(), 'weather_api.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/create-account', methods=['POST'])
def create_account():
    """
    Receives a JSON payload containing 'username' and 'password', and stores
    the user in the database with a salted, hashed password.

    Returns:
        JSON: Success or error message.
    """  
    data = request.json
    try:
        Users.create_account(username=data['username'], password=data['password']) 
        return jsonify({'message': 'Account created successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    """
    Validates the provided 'username' and 'password' against the database.

    Returns:
        JSON: Success message if login is successful, or error message if credentials are invalid.
    """
    data = request.json
    try:
        if Users.check_password(username=data['username'], password=data['password']):
            return jsonify({'message': 'Login successful'}), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@app.route('/update-password', methods=['POST'])
def update_password():
    """
    Receives a JSON payload containing 'username' and 'new_password', and updates
    the stored password in the database after rehashing.

    Returns:
        JSON: Success message if password update is successful, or error message if user is not found.
    """
    data = request.json
    try:
        Users.update_password(username=data['username'], new_password=data['new_password'])
        return jsonify({'message': 'Password updated successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created!")
    app.run(debug=True)
