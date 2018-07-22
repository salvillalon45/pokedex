from flask import Flask, request, redirect, url_for, render_template
from twilio.twiml.messaging_response import MessagingResponse
import json
import requests
from twilio.rest import Client


# Google App Engine does not work with "requests",
# we need to also use "requests-toolbelt" along with it.
# https://stackoverflow.com/questions/40511994/how-should-i-fix-chunkedencodingerror
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

# Twilio Account Information
TWILIO_ACCOUNT_SID = "N"
TWILIO_AUTH_TOKEN = "N"
TWILIO_NUMBER = "N"


# Creating an instance of Flask with __name__ being the name of
# the module
app = Flask(__name__)


BASE_URL = "http://pokeapi.co"


# query_pokeapi
# This function takes a single parameter (the request
# url) and creates python representation of the json data
# ---------------------------------------------------------
def query_pokeapi(resource_uri):
    url = "{0}{1}".format(BASE_URL, resource_uri)
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.text)
    return None

# home()
# Renders the home page for this application
# ---------------------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")


# incoming_message()
# Respond to incoming calls with a MMS message.
# ---------------------------------------------------------
@app.route("/sms", methods=["GET", "POST"])
def incoming_message():
    # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Start our TwiML response
    twiml = MessagingResponse()

    # Get the Body of the inbound SMS message well be expecting
    # from Twilio and makes sure that
    # - removes white space from both ends
    # - it is lowercase
    # - remove any whitespace from between letters is applied to it
    body = request.values.get("Body","").lower().strip().replace(" ","")

    # Poke Api URL
    pokemon_url = "/api/v2/pokemon/{0}/".format(body)

    # query_pokeapi returns the json based on the request from the user
    pokemon_json = query_pokeapi(pokemon_url)

    # In case the user texts something that is not a pokemon name
    if pokemon_json == None:
        msg = twiml.message("Something went wrong! Try 'Pikachu' or 'Rotom'")
        return str(twiml)

    elif pokemon_json:
        # The image of the request Pokemon
        sprite_uri = pokemon_json["sprites"]["front_default"]
        image = sprite_uri

        # The Pokedex description of the request Pokemon
        pokemon_pokedex_entry = query_pokeapi("/api/v2/pokemon-species/{0}/".format(body))

        # Looking for the English Pokedex Description
        for i in pokemon_pokedex_entry["flavor_text_entries"]:
            if i["language"]["name"] == "en":
                message_dex = i["flavor_text"]
                break

        frm = request.values.get("FROM", "")
        # We know it is a UK phone number and we want to send back
        # just an standard SMS, otherwise we send back an MMS
        if "+44" in frm:
            twiml.message("{0} {1}".format(message_dex, image))
            return str(twiml)

        # Otherwise we send back an MMS
        # Adding text message
        msg = twiml.message(message_dex)

        # Adding a picture
        msg.media(image)

        # Return the text message
        # client.messages.create(body=twiml,
        #                 from_=TWILIO_NUMBER,
        #                 to="+17603358201")
        return str(twiml)

if __name__ == "__main__":
    app.run(debug=True)
