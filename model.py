"""Models and database functions for humano db."""

from flask_sqlalchemy import SQLAlchemy

# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

# Compose ORM

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    # User will decide whether to input full last name or initial
    last_name = db.Column(db.String(50), nullable=False)
    # send a confirmation email to this address
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        """Show info about user"""

        return "<User id={} Username={} Email={} Phone{}>".format(self.user_id, 
            self.username, self.email, self.phone_number)


class Message(db.Model):
    """User's message model"""

    __tablename__ = "messages"

    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    message = db.Column(db.String(500), nullable=False)

    # defining relationships
    user = db.relationship("User", backref="messages")

    def __repr__(self):
        """Show info about user's messages"""

        return "<Message id={} Message={}>".format(self.message_id, self.message)

class Contact(db.Model):
    """User's Contact model"""

    __tablename__ = "contacts"

    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    contact_phone_number = db.Column(db.String(20), nullable=False)
    relationship = db.Column(db.String(20), nullable=True)
    contact_name = db.Column(db.String(25), nullable=True)

    # defining relationships
    user = db.relationship("User", backref="contacts")

    def __repr__(self):
        """Show info about a user's contact"""

        return """<Contact id={}, Phone Number={}, Relationship={},Contact 
            Name={}>""".format(self.contact_id, self.contact_phone_number, 
            self.relationship, self.contact_name)


class SentMessage(db.Model):
    """Sent-Message Information model"""

    __tablename__ = "sent_messages"

    sent_message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    message_id = db.Column(db.Integer,
                        db.ForeignKey("messages.message_id"),
                        nullable=False)
    contact_id = db.Column(db.Integer,
                        db.ForeignKey("contacts.contact_id"),
                        nullable=False)
    date_created = db.Column(db.DateTime, nullable=True)
    message_sid = db.Column(db.String(36), nullable=True)
    error_code = db.Column(db.String(20), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # defining relationships
    user = db.relationship("User", backref="messages_sent")
    message = db.relationship("Message", backref="sent_messages")
    contact = db.relationship("Contact", backref="message_sent")

    def __repr__(self):
        """Show info about Sent Messages"""

        return """<Sent Message id={}, Date Created={}, Message sid={}, 
            Error Code={}, Latitude={}, Longitude={}>""".format(self.sent_message_id, self.date_created, 
            self.message_sid, self.error_code, self.latitude, self.longitude)


##############################################################################
# Helper functions


def connect_to_db(app, db_uri='postgresql:///humano'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

