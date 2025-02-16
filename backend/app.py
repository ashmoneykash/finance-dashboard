from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'  # Database file will be created in the project directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

# Create the database tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Finance Dashboard!"})


# User registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# User login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful", "user_id": user.id}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)