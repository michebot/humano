"""Utility file to seed humano database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Message
from model import Contact
from model import SentMessage

from model import connect_to_db, db
from server import app
from datetime import datetime

# create test data

def load_users():
    """Load users from users file into database"""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read user file and insert data
    for row in open("seed_data/users.csv"):
        row = row.rstrip()
        username, first_name, last_name, email, password, phone_number = row.split(",")

        user = User(username=username, first_name=first_name, last_name=last_name, 
                    email=email, password=password, phone_number=phone_number)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, commit work
    db.session.commit()

def load_contacts():
    """Load contacts from contacts file into database"""

    print("Contacts")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Contact.query.delete()

    # Read user file and insert data
    for row in open("seed_data/contacts.csv"):
        row = row.rstrip()
        user_id, contact_phone_number, relationship, contact_name = row.split(",")

        contact = Contact(user_id=user_id, contact_phone_number=contact_phone_number, 
                        relationship=relationship, contact_name=contact_name)

        # We need to add to the session or it won't ever be stored
        db.session.add(contact)

    # Once we're done, commit work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data, comment out when don't want to poplulate db
    load_users()
    load_contacts()


