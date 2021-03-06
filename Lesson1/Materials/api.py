# e5e4cd692a72b0b66ea0a6b80255d1c3
# http://api.openweathermap.org/data/2.5/weather?q=moscow&appid=e5e4cd692a72b0b66ea0a6b80255d1c3

import requests
from pprint import pprint
main_link = 'http://api.openweathermap.org/data/2.5/weather'
params = {'q':'moscow',
          'appid':'e5e4cd692a72b0b66ea0a6b80255d1c3'}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
           'Accept':'*/*'}

response = requests.get(main_link, params=params, headers=headers)
j_body = response.json()

#pprint(j_body)
print(f"В городе {j_body.get('name')} сейчас {j_body.get('main').get('temp') - 273.15: .2f} градусов")