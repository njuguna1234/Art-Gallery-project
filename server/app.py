from flask import Flask, make_response, jsonify, request, url_for, redirect, session
# from models import User, Artwork, Review, app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_cors import CORS
import bcrypt
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_artist = db.Column(db.Boolean, default=False)
    artworks = db.relationship('Artwork', backref='artist', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    serialize_only = ('id', 'name', 'email', 'is_artist')

    def __repr__(self) -> str:
        return f"{self.name}"

class Artwork(db.Model, SerializerMixin):
    __tablename__ = 'artwork'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviews = db.relationship('Review', backref='artwork', lazy=True)

    serialize_only = ('id', 'title', 'description', 'price', 'artist_id')
    
    def __repr__(self) -> str:
        return f"{self.title}"

class Purchase(db.Model, SerializerMixin):
    __tablename__ = 'purchase'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Optional relationships to easily access related data
    user = db.relationship('User', backref='purchases')
    artwork = db.relationship('Artwork', backref='purchases')
    
    serialize_only = ('id', 'user_id', 'artwork_id', 'purchase_date')
    
    def __repr__(self) -> str:
        return f"Purchase(user_id={self.user_id}, artwork_id={self.artwork_id}, date={self.purchase_date})"


class Review(db.Model, SerializerMixin):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)

    serialize_only = ('id', 'content', 'rating', 'user_id', 'artwork_id')
    
    def __repr__(self) -> str:
        return f"{self.content}"

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/register', methods=['POST'])
def register():
    # Ensure the request is JSON
    if not request.is_json:
        return jsonify({'message': 'Content-Type must be application/json'}), 415  # Unsupported Media Type

    data = request.get_json()

    # Check for required fields
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400  # Bad request status

    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409  # Conflict status

    # Hash the password for security
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    # Create new user
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        is_artist=data.get('is_artist', False)
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/register', methods=['GET'])
def get_registration_info():
    return jsonify({
        'message': 'Send a POST request to register a user.',
        'example_request': {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'securepassword',
            'is_artist': False
        }
    }), 200

# View to get users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    
    if users:
        return make_response(jsonify([user.to_dict() for user in users]), 200)
    else:
        error_message = {
            "message": f"User {id} not found."
        }
        return make_response(jsonify(error_message), 404)

# View to get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    
    if user:
        response_body = {
            "id": user.id,
            "name": user.name,
            "magnitude": user.email,
            "year": user.is_artist,
        }
        return make_response(jsonify(response_body), 200)
    else:
        error_message = {
            "message": f"User {id} not found."
        }
        return make_response(jsonify(error_message), 404)
    
# View to update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    
    if not user:
        return make_response(jsonify({"message": f"User {id} not found."}), 404)

    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'is_artist' in data:
        user.is_artist = data['is_artist']

    db.session.commit()
    
    return make_response(jsonify({'message': 'User updated successfully'}), 200)

# View to delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({'message': 'User deleted successfully'}), 200)
    else:
        return make_response(jsonify({'message': f'User {id} not found.'}), 404)

# Improved login route
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'message': 'Content-Type must be application/json'}), 415

    data = request.get_json()

    # Check for required fields
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        session['username'] = user.name
        return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


# View to create a new artwork
@app.route('/artworks', methods=['POST'])
def create_artwork():
    if not request.is_json:
        return jsonify({'message': 'Content-Type must be application/json'}), 415

    data = request.get_json()
    required_fields = ['title', 'description', 'price', 'artist_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    new_artwork = Artwork(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        artist_id=data['artist_id']
    )

    db.session.add(new_artwork)
    db.session.commit()
    
    return jsonify({'message': 'Artwork created successfully'}), 201

# View to get all artworks
@app.route('/artworks', methods=['GET'])
def get_artworks():
    artworks = Artwork.query.all()
    if artworks:
        return make_response(jsonify([artwork.to_dict() for artwork in artworks]), 200)
    else:
        error_message = {
            "message": "No artworks found."
        }
        return make_response(jsonify(error_message), 404)

# View to get an artwork by id
@app.route('/artworks/<int:id>', methods=['GET'])
def get_artwork_by_id(id):
    artwork = Artwork.query.get(id)
    
    if artwork:
        return make_response(jsonify(artwork.to_dict()), 200)
    else:
        error_message = {
            "message": f"Artwork {id} not found."
        }
        return make_response(jsonify(error_message), 404)

# View to update an artwork
@app.route('/artworks/<int:id>', methods=['PUT'])
def update_artwork(id):
    artwork = Artwork.query.get(id)
    
    if not artwork:
        return make_response(jsonify({"message": f"Artwork {id} not found."}), 404)

    data = request.get_json()
    if 'title' in data:
        artwork.title = data['title']
    if 'description' in data:
        artwork.description = data['description']
    if 'price' in data:
        artwork.price = data['price']

    db.session.commit()
    
    return make_response(jsonify({'message': 'Artwork updated successfully'}), 200)

# View to delete an artwork
@app.route('/artworks/<int:id>', methods=['DELETE'])
def delete_artwork(id):
    artwork = Artwork.query.get(id)
    
    if artwork:
        db.session.delete(artwork)
        db.session.commit()
        return make_response(jsonify({'message': 'Artwork deleted successfully'}), 200)
    else:
        return make_response(jsonify({'message': f'Artwork {id} not found.'}), 404)

# View to create a new review
@app.route('/reviews', methods=['POST'])
def create_review():
    if not request.is_json:
        return jsonify({'message': 'Content-Type must be application/json'}), 415

    data = request.get_json()
    required_fields = ['content', 'rating', 'user_id', 'artwork_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    new_review = Review(
        content=data['content'],
        rating=data['rating'],
        user_id=data['user_id'],
        artwork_id=data['artwork_id']
    )

    db.session.add(new_review)
    db.session.commit()
    
    return jsonify({'message': 'Review created successfully'}), 201

# View to get all reviews
@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return make_response(jsonify([review.to_dict() for review in reviews]), 200)

# View to get a review by id
@app.route('/reviews/<int:id>', methods=['GET'])
def get_review_by_id(id):
    review = Review.query.get(id)
    
    if review:
        return make_response(jsonify(review.to_dict()), 200)
    else:
        error_message = {
            "message": f"Review {id} not found."
        }
        return make_response(jsonify(error_message), 404)

# View to update a review
@app.route('/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    review = Review.query.get(id)
    
    if not review:
        return make_response(jsonify({"message": f"Review {id} not found."}), 404)

    data = request.get_json()
    if 'content' in data:
        review.content = data['content']
    if 'rating' in data:
        review.rating = data['rating']

    db.session.commit()
    
    return make_response(jsonify({'message': 'Review updated successfully'}), 200)

# View to delete a review
@app.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get(id)
    
    if review:
        db.session.delete(review)
        db.session.commit()
        return make_response(jsonify({'message': 'Review deleted successfully'}), 200)
    else:
        return make_response(jsonify({'message': f'Review {id} not found.'}), 404)

@app.route('/artworks/<int:artwork_id>/purchase', methods=['POST'])
def purchase_artwork(artwork_id):
    data = request.json
    purchase = Purchase(
        user_id=data['user_id'],
        artwork_id=artwork_id
    )
    db.session.add(purchase)
    db.session.commit()
    return jsonify(purchase.to_dict()), 201

@app.route('/users/<int:user_id>/purchases', methods=['GET'])
def get_user_purchases(user_id):
    purchases = Purchase.query.filter_by(user_id=user_id).all()
    return jsonify([purchase.to_dict() for purchase in purchases])


if __name__ == '__main__':
    app.run(debug=True)
