import requests


def get_current_rate():
    url = "https://api.apilayer.com/fixer/convert?to=RUB&from=USD&amount=1"
    header = {"apikey": "M3ZLsRpZnrb80mAb6ZobImQWTo8oe2qg"}

    response = requests.get(url, headers=header)
    response = response.json()
    return response['info']['rate']