import requests as req
from api_key import API_KEY

BASE_URL = 'https://v6.exchangerate-api.com/v6'

def get_conversion_rate(base_currency: str, target_currency: str):
    result = req.get(f'{BASE_URL}/{API_KEY}/pair/{base_currency}/{target_currency}')
    if result.status_code == 200:
        return result.json()['conversion_rate']
    return None
    