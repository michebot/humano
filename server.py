"""Flask server.
"""

from jinja2 import StrictUndefined

from flask import (Flask, redirect, request, jsonify, render_template, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
# look into what these are
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABCDEFGHIJ"


@app.route("/")
def show_index():
    """Return homepage"""

    return render_template("index.html")


@app.route("/sign-up")
def register_user():
    """Show the assessment page."""

    return render_template("sign-up.html")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # added this to stop redirect page request
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0")