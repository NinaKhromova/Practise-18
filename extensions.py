import requests
import json
from config import keys

class ConvertionException(Exception):
    pass
class CryptoConverter:
   @staticmethod
   def convert(quote: str, base: str, amount: str):
       if quote == base:
           raise ConvertionException(f'Не могу перевести одинаковые валюты {base}')

       try:
           quote_ticker = keys[quote]
       except KeyError:
           raise ConvertionException(f'В моей базе нет валюты {quote}\n\
список доступных валют /values')

       try:
           base_ticker = keys[base]
       except KeyError:
           raise ConvertionException(f'В моей базе нет валюты {base}\n\
список доступных валют /values ')


       try:
           amount = float(amount)
       except ValueError:
           raise ConvertionException(f'Не удалось обработать количество {amount}')



       r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
       return json.loads(r.content)[keys[base]]*amount

