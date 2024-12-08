from flask import Flask, request, jsonify
from database.user_model import Users
from config import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/create-account', methods=['POST'])
def create_account():
    data = request.json
    try:
        Users.create_account(username=data['username'], password=data['password'])  # Correct method call
        return jsonify({'message': 'Account created successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        if Users.check_password(username=data['username'], password=data['password']):
            return jsonify({'message': 'Login successful'}), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@app.route('/update-password', methods=['POST'])
def update_password():
    data = request.json
    try:
        Users.update_password(username=data['username'], new_password=data['new_password'])
        return jsonify({'message': 'Password updated successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
