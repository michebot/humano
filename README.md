# Humano

## Summary

**Humano** is an app that helps users prepare for an encounter with ICE or law enforcement and quickly informs a user’s network if they worry they may be detained. Humano was designed for undocumented immigrants who are in fear of being detained or deported by law enforcement, however it could be a general platform for emergency notifications. A customized message along with the user's location is sent to their network at the click of a button using the Twilio and Google Maps API. Once a user has set up their account, Humano provides resources to help educate users about their legal rights,  search for lawyers in their area (using the Google Places and Google Details APIs), and get the most recent news regarding immigration (using the News API).

## About the Developer

Humano was created by Michelle Espinosa, a software engineer in San Francisco, CA. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/michelle-espinosa/).

## Technologies

**Tech Stack:**

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Jinja2
- HTML
- CSS
- Javascript
- JQuery
- AJAX
- JSON
- Bootstrap
- Python unittest module
- Twilio API
- Google Maps JavaScript API
- Google Places API
- Google Details API
- News API

Humano is an app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM. The front end templating uses Jinja2, the HTML was built using Bootstrap, and the Javascript uses JQuery and AJAX to interact with the backend. Humano was deployed with AWS Lightsail and can be found at [humano.us](humano.us). *Currently working on getting an SSL certificate.*