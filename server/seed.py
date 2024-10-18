from app import app, db
from models import User, Artwork, Review, Purchase
from datetime import datetime
from werkzeug.security import generate_password_hash


# Drop all tables and recreate them
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create some users (some artists, some regular users)
    artist1 = User(
        name="Vincent van Gogh", 
        email="vangogh@example.com", 
        password=generate_password_hash("password123"), 
        is_artist=True
    )
    artist2 = User(
        name="Pablo Picasso", 
        email="picasso@example.com", 
        password=generate_password_hash("password123"), 
        is_artist=True
    )
    user1 = User(
        name="John Doe", 
        email="johndoe@example.com", 
        password=generate_password_hash("password123"), 
        is_artist=False
    )
    user2 = User(
        name="Jane Smith", 
        email="janesmith@example.com", 
        password=generate_password_hash("password123"), 
        is_artist=False
    )

    # Add users to the session
    db.session.add_all([artist1, artist2, user1, user2])
    db.session.commit()

    # Create some artworks for the artists
    artwork1 = Artwork(
        title="Starry Night",
        description="A beautiful night sky painting by van Gogh",
        price=500.00,
        artist_id=artist1.id
    )
    artwork2 = Artwork(
        title="The Old Guitarist",
        description="A masterpiece by Picasso",
        price=750.00,
        artist_id=artist2.id
    )
    artwork3 = Artwork(
        title="Sunflowers",
        description="Another great piece by van Gogh",
        price=300.00,
        artist_id=artist1.id
    )

    # Add artworks to the session
    db.session.add_all([artwork1, artwork2, artwork3])
    db.session.commit()

    # Create some reviews
    review1 = Review(
        content="Amazing artwork! The colors are so vibrant.",
        rating=5,
        user_id=user1.id,
        artwork_id=artwork1.id
    )
    review2 = Review(
        content="A true masterpiece. Worth every penny.",
        rating=5,
        user_id=user2.id,
        artwork_id=artwork2.id
    )
    review3 = Review(
        content="Great piece, but a bit overpriced for me.",
        rating=4,
        user_id=user1.id,
        artwork_id=artwork3.id
    )

    # Add reviews to the session
    db.session.add_all([review1, review2, review3])
    db.session.commit()

    # Create purchases
    purchase1 = Purchase(
        user_id=user1.id,
        artwork_id=artwork1.id,
        purchase_date=datetime.utcnow()
    )
    purchase2 = Purchase(
        user_id=user2.id,
        artwork_id=artwork2.id,
        purchase_date=datetime.utcnow()
    )

    # Add purchases to the session
    db.session.add_all([purchase1, purchase2])
    db.session.commit()

    print("Database seeded successfully!")
