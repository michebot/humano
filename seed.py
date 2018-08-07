"""Utility file to seed humano database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Message
from model import Contact
from model import SentMessage

from model import connect_to_db, db
from server import app
from datetime import datetime















if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data