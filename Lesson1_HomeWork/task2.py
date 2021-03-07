import requests
import json

url = "https://flight-data4.p.rapidapi.com/get_airline_flights"

params = {"airline": "AFL"}

headers = {
    'x-rapidapi-key': "ec8bd94033msh7e34f65c59fba16p18be8djsnbe425e0e155b",
    'x-rapidapi-host': "flight-data4.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=params)

# Сохранение в файл

with open(f'{"info_" + params.get("airline")}.json', 'w') as outfile:
    json.dump(response.json(), outfile)

# Печать результата

print(f'Found {len(response.json())} flights in the sky on request'
      f' {params.get("airline")}:\n'
      f'{"_" * 55}\n'
      f'|{"Flight": ^15}'
      f'|{"Departure": ^10}'
      f'|{"Arrival": ^10}'
      f'|{"Aircraft_type": ^15}|'
      f'\n{"-" * 55}')
flights = response.json()

for flight in flights:
    print(f'|{flight.get("flight") + " ": >15}'
          f'|{flight.get("departure") + " ": >10}'
          f'|{flight.get("arrival") + " ": >10}'
          f'|{flight.get("type") + " ": >15}|')

"""
Found 24 flights in the sky on request AFL:

_______________________________________________________
|    Flight     |Departure | Arrival  | Aircraft_type |
-------------------------------------------------------
|         SU323 |      MLE |      SVO |          B77W |
|        SU1125 |      AER |      SVO |          A321 |
|        SU1445 |      IKT |      SVO |          B738 |
|         SU521 |      DXB |      SVO |          B77W |
|        SU1700 |      SVO |      VVO |          B77W |
|        SU2579 |      LHR |      SVO |          A321 |
|        SU2280 |      SVO |      IST |          A320 |
|        SU2143 |      AYT |      SVO |          B738 |
|        SU1730 |      SVO |      PKC |          B77W |
|        SU2133 |      IST |      SVO |          A320 |
|        SU1316 |      SVO |      MMK |          SU95 |
|        SU1006 |      SVO |      KGD |          A320 |
|        SU1625 |      SIP |      SVO |          B738 |
|        SU1359 |      GSV |      SVO |          SU95 |
|          SU26 |      SVO |      LED |          A320 |
|        SU1365 |      STW |      SVO |          SU95 |
|        SU1249 |      REN |      SVO |          B738 |
|        SU1143 |      AAQ |      SVO |          SU95 |
|        SU1405 |      SVX |      SVO |          B738 |
|        SU1011 |      KGD |      SVO |          A320 |
|        SU1293 |      IJK |      SVO |          SU95 |
|        SU1325 |      MMK |      SVO |          A320 |
|        SU2381 |      GVA |      SVO |          A321 |
|        SU1059 |      MCX |      SVO |          A320 |

"""