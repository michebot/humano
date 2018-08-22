"""Flask server.
"""

from jinja2 import StrictUndefined

from flask import (Flask, redirect, request, jsonify, render_template, flash, 
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Contact, Message, SentMessage, connect_to_db, db

from twilio_call import send_message_to_recipients

import os

app = Flask(__name__)
# look into what these are
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['FLASK_SECRET_KEY']

# GOOGLE MAPS KEY
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
    # if above query returns None (i.e. username not in database)
    if not check_username:
        new_user = User(username=username, first_name=first_name, 
                        last_name=last_name, email=email, password=password,
                        phone_number=phone_number)

        db.session.add(new_user)
        db.session.commit()
        flash("Welcome!")

        print("\n\n\nUSER ADDED\n\n\n")

        return redirect("/")

    else:
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

    # if user is found in db
    elif user is not None:
        if user.password != password:
            flash("Incorrect password, please try again.")
            return redirect("/login")

        elif username == user.username and password == user.password:
            session["user_id"] = user.user_id
            flash("Welcome!")

            print("\n\n\nUSER LOGGED IN\n\n\n")
            return redirect("/user-home")


@app.route('/logout', methods=['GET'])
def log_out():
    """Log user out."""

    del session["user_id"] 
    # session["user_id"] = None

    flash("You have been logged out.")
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
        return render_template("user-home.html", user_name=user_name, contacts=users_contacts, message=users_message)
    else:
        flash("Please Log In or Sign Up")
        return redirect('/')



### USER CREATING PROFILE: ADDING/VIEWING/EDITING CONTACTS AND MESSAGE ###
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

        return redirect("/user-home")

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
    """Update the user's contact information in the DB"""

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

    return redirect("/user-home")


# add route for viewing message
# add route for editing message

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


    # need to change so that we can check if there is a current message 
    # and if there is, allow user to edit message
    # if not check_contact_phone_number:
    #     new_contact = Contact(user_id=current_user, contact_name=contact_name, 
    #                           relationship=relationship,
    #                           contact_phone_number=contact_phone_number)

        # db.session.add(new_contact)
        # db.session.commit()
        # flash("Welcome!")

        # print("\n\n\nMESSAGE ADDED\n\n\n")

        # return redirect("/user-home")

    # else:
    #     flash("It looks like you've already added a contact with this phone number.")
    #     return redirect("/user-home")



### SENDING MESSAGE AND MAP ROUTES ###
@app.route("/send-message.json", methods=["POST"])
def send_message():
    """Processes button request to send messages to user's contacts"""

    # getting current user in session
    current_user = session.get("user_id")
    contacts = Contact.query.filter(Contact.user_id == current_user).all()
    # will need to change this query to get the most up to date message (order by date)
    message = Message.query.filter(Message.user_id == current_user).first()

    # getting user's location from front-end
    user_lat = float(request.form.get("lat"))
    user_lng = float(request.form.get("lng"))
    user_location = str([user_lat, user_lng])
    link = "https://www.google.com/maps/?q={lat},{lng}".format(lat=user_lat, lng=user_lng)

    for contact in contacts:
        message_results = send_message_to_recipients(contact.contact_phone_number, 
                                                     message.message)
        # import pdb; pdb.set_trace()
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

    flash("Your message has been sent.")
    return jsonify({"success": "true"})



@app.route("/map")
def render_map():
    """Render map with user's location."""

    return render_template("map.html", key=GOOGLE_API_KEY)

@app.route("/map-coordinates.json", methods=["GET"])
def obtain_users_coordinates():
    """Obtain user's location from DB and send to front-end as a JSON"""

    current_user = session.get("user_id")

    current_location = SentMessage.query.filter(SentMessage.user_id==current_user)\
                                        .order_by(SentMessage.date_created.desc()).first()

    return jsonify({"lat": current_location.latitude, "lng": current_location.longitude})



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