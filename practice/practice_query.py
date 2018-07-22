# importing requests
import requests
import json

url = "http://pokeapi.co/api/v2/pokemon/pikachu"

# In line 8 I am making a request to an API called PokeAPI. I get back a response
response = requests.get(url);

if response.status_code == 200:
    data = json.loads(response.text)
    print(data['name'])
    # print(data["url"])
    print(data["stats"])

else:
    print("An error occurred querying the API")
