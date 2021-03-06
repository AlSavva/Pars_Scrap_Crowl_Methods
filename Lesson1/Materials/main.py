import requests

url = 'https://www.google.ru'

response = requests.get(url)

if response.status_code == 200:
    pass
else:
    pass

if response.ok:
    pass
else:
    pass

print(response.encoding)
print(response.headers.get('Content-Type'))

response.text
response.content

response.url

print()