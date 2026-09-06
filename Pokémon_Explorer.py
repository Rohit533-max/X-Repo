import requests
def get_pokemon(name):  
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    return data

def basic_info(data):
    return {
        "name": data["name"],
        "height": data["height"] / 10,
        "weight": data["weight"] / 10,

        "types": [
            item["type"]["name"]
            for item in data["types"]
        ],

        "abilities": [
            item["ability"]["name"]
            for item in data["abilities"]
        ],

        "image": data["sprites"]["front_default"],

        "stats": {
            item["stat"]["name"]: item["base_stat"]
            for item in data["stats"]
        }
    }

def compare_pokemon(name1, name2):
    pokemon1 = get_pokemon(name1)
    pokemon2 = get_pokemon(name2)

    return {
        "pokemon1": basic_info(pokemon1),

        "pokemon2": basic_info(pokemon2)
    }


def main(name):
    try:
        pokemon = get_pokemon(name)
        return basic_info(pokemon)

    except requests.HTTPError:
        return {"error": "Pokémon not found"}

    except requests.RequestException:
        return {"error": "Could not connect to the Pokémon API"}


if __name__ == "__main__":
    name = input("Enter Pokémon name: ")
    main(name)
