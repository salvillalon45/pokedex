import requests
import json

BASE_URL = "http://pokeapi.co"


# query_pokeapi
# This function takes a single parameter (the request
# url) and creates python representation of the json data
# ---------------------------------------------------------
def query_pokeapi(resource_url):
    url = "{0}{1}".format(BASE_URL, resource_url)
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.text)
    return None

# Manually creating a charizard request
# The variable charizard represents the json output of the
# API charizard request
charizard = query_pokeapi("/api/v2/pokemon/charizard/")
charizard_pokedex_entry = query_pokeapi("/api/v2/pokemon-species/charizard")


# This will give us URLs that we can use in the query_pokeapi function
# One for the sprite
# One for the Pokedex Description
sprite_uri = charizard["sprites"]["front_default"]

# Getting Json out of the requests
# sprite = query_pokeapi(sprite_uri)
# description = query_pokeapi(description_uri)

# POKEMON NAME
print("POKEMON NAME")
print(charizard["name"])
print("---------------------------------------")

# POKEDEX ENTRY
print("POKEMON ENTRY")
print(charizard_pokedex_entry["flavor_text_entries"][1]["flavor_text"])
print("---------------------------------------")

# POKEDEX FROM WHICH GAME
print("POKEDEX FROM WHICH GAME")
print(charizard_pokedex_entry["flavor_text_entries"][1]["version"]["name"])
print("---------------------------------------")

# POKEMON IMAGE
print("POKEMON IMAGE URL")
print(sprite_uri)
print("---------------------------------------")
