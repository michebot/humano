"""Flask server.
"""

from jinja2 import StrictUndefined

from flask import (Flask, redirect, request, jsonify, render_template, flash, 
                   session)

from flask_debugtoolbar import DebugToolbarExtension

import os, bcrypt

from model import User, Contact, Message, SentMessage, connect_to_db, db



app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True



### IMPORTING API HELPER FXs ###
from twilio_api_call import send_message_to_recipients
from news_api_call import obtain_news
from google_places_api_call import lawyer_search_google_api_call
from google_place_details_api_call import lawyer_details_api_call



### KEYS ###
# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['FLASK_SECRET_KEY']
# Google Maps JS API Key
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]



### HOMEPAGE ROUTE ###
@app.route("/")
def get_index():
    """Return homepage with login or sign up links"""

    return render_template("index.html")



### SIGN UP ROUTES ###
@app.route("/sign-up", methods=["GET"])
def register_user():
    """Render form for user sign up."""

    return render_template("sign-up.html")

@app.route("/sign-up", methods=["POST"])
def process_user_info():
    """Save user's information to our database."""

    username = request.form.get("username")
    first_name = request.form.get("first_name").capitalize()
    last_name = request.form.get("last_name").capitalize()
    email = request.form.get("email")
    password = request.form.get("password")
    phone_number = request.form.get("phone_number")

    # if the username is already in our database, will return True
    # import pdb; pdb.set_trace()
    check_username = User.query.filter(User.username==username).first()

    # salt and hash password
    b_password = password.encode('utf-8')
    h_password = bcrypt.hashpw(b_password, bcrypt.gensalt())

    # if above query returns None (i.e. username not in database)
    if not check_username:
        new_user = User(username=username, 
                        first_name=first_name, 
                        last_name=last_name, 
                        email=email, 
                        password=h_password.decode('utf-8'),
                        phone_number=phone_number)

        db.session.add(new_user)
        db.session.commit()
        flash("Welcome! Thanks for signing up!")

        print("\n\n\nUSER ADDED\n\n\n")

        session["user_id"] = new_user.user_id

        return redirect("/user-home")

    else:
        flash("""Looks like this username is taken, please select a different 
                 username. \n Or you might already have an 
                 account with us! If so, please log in.""")
        return redirect("/")



### LOGIN(OUT) ROUTES ###
@app.route("/login", methods=["GET"])
def login_user():
    """Renders form for user to login"""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_user_login():
    """Gets user's login info and renders user homepage"""

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter(User.username==username).first()

    # if user not in db
    if not user:
        flash("We couldn't find this username. Please try again or Sign Up.")
        return redirect("/")

    # user exists
    elif user:

        # if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        #     flash("Incorrect password, please try again.")
        #     return redirect("/login")

        if username == user.username and bcrypt.checkpw(password.encode('utf-8'), 
                                                        user.password.encode('utf-8')):
            session["user_id"] = user.user_id
            flash("Welcome!")
            print("\n\n\nUSER LOGGED IN\n\n\n")
            return redirect("/user-home")

        else:
            flash("Incorrect password, please try again.")
            return redirect("/login")


@app.route('/logout', methods=['GET'])
def log_out():
    """Log user out."""

    del session["user_id"] 
    # session["user_id"] = None

    flash("You have been logged out. See you soon!")
    print("\n\n\nUSER LOGGED OUT\n\n\n")

    return redirect("/")


### USER HOMEPAGE ###
@app.route("/user-home")
def display_user_homepage():
    """Displays once user logins"""

    # getting user in session
    current_user = session.get('user_id')

    if current_user:
        user = User.query.filter(User.user_id == current_user).first()
        user_name = user.first_name.capitalize()
        users_contacts = Contact.query.filter(Contact.user_id == current_user).all()
        users_message = Message.query.filter(Message.user_id == current_user).first()
        users_sent_message = SentMessage.query.filter(SentMessage.user_id == current_user).all()
        return render_template("user-home.html", current_user=current_user, user_name=user_name, 
                                contacts=users_contacts, message=users_message, 
                                users_sent_message=users_sent_message)
    else:
        flash("Please Log In or Sign Up")
        return redirect('/')



### USER CREATING PROFILE: ADDING/VIEWING/EDITING CONTACTS AND MESSAGE ###

### USER'S CONTACTS ###
@app.route("/add-contact", methods=["GET"])
def add_users_contact():
    """Renders form for user to add contacts"""

    # getting current user in session
    current_user = session.get("user_id")

    if current_user:
        user = User.query.filter(User.user_id == current_user).first()
        user_name = user.first_name.capitalize()

        return render_template("add-contact.html")
    else:
        flash("Please Log In or Sign Up.")
        return redirect('/')


@app.route("/add-contact", methods=["POST"])
def process_users_contact_info():
    """Save user's contact information to our database"""

    # getting current user in session
    current_user = session.get("user_id")

    contact_phone_number = request.form.get("contact_phone_number")
    relationship = request.form.get("relationship")
    contact_name = request.form.get("contact_name").capitalize()

    # if the contact is already in our database, will return True
    # import pdb; pdb.set_trace()
    check_contact_phone_number = Contact.query.filter(Contact.contact_phone_number == 
                                                      contact_phone_number, 
                                                      Contact.user_id == 
                                                      current_user).first()
    # if above query returns None (i.e. username not in database)
    if not check_contact_phone_number:
        new_contact = Contact(user_id=current_user, contact_name=contact_name, 
                              relationship=relationship,
                              contact_phone_number=contact_phone_number)

        db.session.add(new_contact)
        db.session.commit()
        flash("Your contact has been added.")

        print("\n\n\nCONTACT ADDED\n\n\n")

        return redirect("/my-contacts")

    else:
        flash("It looks like you've already added a contact with this phone number.")
        return redirect("/user-home")


@app.route("/my-contacts")
def display_users_contacts():
    """Renders user's contacts"""

    current_user = session.get("user_id")
    users_contacts = Contact.query.filter(Contact.user_id == current_user).all()

    return render_template("my-contacts.html", current_user=current_user, 
                            contacts=users_contacts)


@app.route("/my-contacts/edit-<contact_id>", methods=["GET"])
def edit_users_contact(contact_id):
    """Allow user to edit their contact's information"""

    current_user = session.get("user_id")

    # contact = Contact.query.get(int(contact_id))
    contact = Contact.query.filter(Contact.contact_id == contact_id).first()

    return render_template("edit-contact.html", contact=contact)


@app.route("/my-contacts/edit-<contact_id>", methods=["POST"])
def update_user_contact_info(contact_id):
    """Update the user's contact information in DB"""

    # getting current user in session
    current_user = session.get("user_id")

    # contact object to edit
    contact = Contact.query.get(int(contact_id))
    # contact = Contact.query.filter(Contact.contact_id == contact_id).first()

    # updated info
    updated_contact_phone_number = request.form.get("contact_phone_number")
    updated_relationship = request.form.get("relationship")
    updated_contact_name = request.form.get("contact_name").capitalize()

    if contact:
        contact.contact_phone_number = updated_contact_phone_number
        contact.relationship = updated_relationship
        contact.contact_name = updated_contact_name

        db.session.commit()
        flash("Your contact has been updated.")

        print("\n\n\nCONTACT EDITED\n\n\n")

    return redirect("/my-contacts")



@app.route("/my-contacts/delete-<contact_id>", methods=["POST"])
def delete_users_contact(contact_id):
    """Delete a user's contact from DB"""

    #getting current user in session
    current_user = session.get("user_id")

    # contact object to edit
    contact = Contact.query.get(int(contact_id))

    db.session.delete(contact)
    db.session.commit()
    
    flash("Your contact has been deleted.")

    print("\n\n\nCONTACT DELETED\n\n\n")

    return redirect("/my-contacts")



### USER'S MESSAGE ###
@app.route("/add-message", methods=["GET"])
def add_users_message():
    """Renders form for user to add their customized message"""

    # getting current user in session
    current_user = session.get("user_id")

    if current_user:
        user = User.query.filter(User.user_id == current_user).first()
        return render_template("add-message.html")
    else:
        flash("Please Log In or Sign Up.")
        return redirect('/')


@app.route("/add-message", methods=["POST"])
def process_users_message():
    """Save user's message to our database"""

    # getting current user in session
    current_user = session.get("user_id")

    message = request.form.get("message")

    new_message = Message(user_id=current_user, message=message)
    db.session.add(new_message)
    db.session.commit()

    flash("Your message has been saved!")

    print("\n\n\nMESSAGE ADDED\n\n\n")

    return redirect("/user-home")


@app.route("/view-message")
def display_users_message():
    """Render the user's message"""

    current_user = session.get("user_id")
    current_message = Message.query.filter(Message.user_id == current_user).first()

    return render_template("view-message.html", message_obj=current_message)


@app.route("/edit-message", methods=["GET"])
def edit_users_message():
    """Renders form for user to edit their message"""

    # getting current user in session
    current_user = session.get("user_id")

    old_message = Message.query.filter(Message.user_id == current_user).first()

    return render_template("edit-message.html", old_message=old_message)

# TODO: CHANGE ME TO ADD A RECORD WHEN A USER UPDATES THEIR MESSAGE
@app.route("/edit-message", methods=["POST"])
def update_users_message():
    """Update the user's message"""

    # getting current user in session
    current_user = session.get("user_id")

    # message object to edit
    old_message = Message.query.filter(Message.user_id == current_user).first()

    updated_message = request.form.get("message")

    if old_message:
        old_message.message = updated_message
        db.session.commit()
        flash("Your message has been updated.")

        print("\n\n\nMESSAGE EDITED\n\n\n")

    return redirect("/user-home")



@app.route("/sent-messages")
def view_sent_messages():
    """Allows a user to see when they have sent a message and to how many
       contacts"""

    # obtain current user in session
    current_user = session.get("user_id")

    # query for timestamps of sent messages
    sent_messages_obj_list = SentMessage.query.filter(SentMessage.user_id==
                                                      current_user)\
                                              .order_by(SentMessage.date_created\
                                              .desc())\
                                              .all()

    # query for message content
    message_content = Message.query.filter()

    # db.session query where i only get the dates created and count those
    dates_created_obj_list = db.session.query(SentMessage.date_created)


    return render_template("sent-messages.html", 
                            sent_messages=sent_messages_obj_list)



### SENDING MESSAGE ROUTES WITH TWILIO API ###
@app.route("/send-message.json", methods=["POST"])
def send_message():
    """Processes button request from user's homepage to send their message and 
       location to user's contacts"""

    # getting current user in session
    current_user = session.get("user_id")
    contacts = Contact.query.filter(Contact.user_id == current_user).all()
    # will need to change this query to get the most up to date message (order by date)
    message = Message.query.filter(Message.user_id == current_user)\
                           .order_by(Message.message_id.desc()).first()

    # getting user's location from front-end in user-home.html
    user_lat = float(request.form.get("lat"))
    user_lng = float(request.form.get("lng"))
    user_location = str([user_lat, user_lng])
    # link = "https://www.google.com/maps/?q={lat},{lng}".format(lat=user_lat, lng=user_lng)
    # link = "http://localhost:5000/map/{user_id}?q={lat},{lng}".format(user_id=current_user,
    #                                                                   lat=user_lat, 
    #                                                                   lng=user_lng)
    link = "http://localhost:5000/map/{user_id}".format(user_id=current_user)


    for contact in contacts:
        message_results = send_message_to_recipients(contact.contact_phone_number, 
                                                     message.message)
        # import pdb; pdb.set_trace()
        # create a new sent_message record
        new_sent_message = SentMessage(user_id=current_user, 
                                       message_id=message.message_id, 
                                       contact_id=contact.contact_id, 
                                       date_created=message_results[1], 
                                       message_sid=message_results[0],
                                       error_code=message_results[2], 
                                       latitude=user_lat, 
                                       longitude=user_lng)
        db.session.add(new_sent_message)
        print("\n\n\nMESSAGE SENT\n\n\n")

        location_results = send_message_to_recipients(contact.contact_phone_number, 
                                                      link)
        print("\n\n\nLOCATION SENT\n\n\n")

    db.session.commit()

    # creating a new instance of the message since prior message has been sent
    new_message = Message(user_id=current_user, message=message.message)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"success": "true"})



### ROUTES TO RENDER MAP WITH USER'S LOCATION ###
@app.route("/map/<user_id>")
def render_map(user_id):
    """Render map with user's location."""

    # pass user id to map template
    user_to_render_location_for = user_id

    # query for user object to render "User's location" on template


    return render_template("map.html", key=GOOGLE_API_KEY, user_id=user_to_render_location_for)


@app.route("/map-coordinates.json", methods=["GET"])
def obtain_users_coordinates():
    """Obtain user's location from DB and send to front-end as a JSON"""

    # DEPRECATED: for when obtaining location from session
    # current_user = session.get("user_id")

    # obtain user_id from hidden inputs from map
    current_user = request.args.get("user_id")

    current_location = SentMessage.query.filter(SentMessage.user_id==current_user)\
                                        .order_by(SentMessage.date_created.desc())\
                                        .first()

    return jsonify({"lat": current_location.latitude, "lng": current_location.longitude})



### ROUTES FOR NEWS ###
@app.route("/news")
def display_news():
    """Render news on immigration from News API"""

    articles = obtain_news()

    return render_template("news.html", articles=articles)



### ROUTES FOR GOOGLE PLACES and GOOGLE DETAILS API - LAWYERS ###
@app.route("/search_lawyers")
def search_for_lawyers():
    """Allow users to search for immigration lawyers using the Google Places API"""

    search_results = lawyer_search_google_api_call()

    next_page_token = search_results["next_page_token"]

    return render_template("lawyer-search.html", results=search_results["results"],
                                                 next_page_token=next_page_token)


@app.route("/search_lawyers/<place_id>")
def search_for_lawyer_details(place_id):
    """Call the Google Details API to obtain a lawyer's details"""

    search_details = lawyer_details_api_call(place_id)

    return render_template("lawyer-details.html", result=search_details["result"])



### HELPER FXs ###

def example_data():
    """Mock user and contact data for testing."""

    User.query.delete()

    mary = User(username="marylamb", first_name="Mary", last_name="Lamb", 
                email="mary@lamb.com", password="password", phone_number="12345678901")
    toby = User(username="tobesmagoats", first_name="Tobias", last_name="Funke", 
                email="tobias@ad.com", password="password", phone_number="12345678902")

    mary_contact = Contact(user_id=1, contact_name="Joseph", relationship="husband",
                           contact_phone_number="17142091862")

    toby_contact = Contact(user_id=2, contact_name="George Michael", 
                           relationship="nephew", contact_phone_number="17142091862")

    db.session.add_all([mary, toby])
    db.session.commit()



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # added this to stop redirect page request
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # connect our app to our database
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0")