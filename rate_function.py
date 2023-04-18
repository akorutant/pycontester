import requests


class APICurrencyRates:
    def __init__(self, api_key, to_currency, from_currency, amount):
        self.api_key = api_key
        self.to_currency = to_currency
        self.from_currency = from_currency
        self.amount = amount

    def get_current_rate(self):
        url = f"https://api.apilayer.com/fixer/convert?to={self.to_currency}" \
              f"&from={self.from_currency}&amount={self.amount}"
        header = {"apikey": self.api_key}

        response = requests.get(url, headers=header)
        response = response.json()
        return response['info']['rate']