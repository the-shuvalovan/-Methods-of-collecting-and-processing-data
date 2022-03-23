import requests
import json

url = 'https://api.rasp.yandex.net/v3.0/schedule/'
key = '868bb776-6ace-44a5-868b-ca2cb5f83d6b'

#2024000 - код станции Самара согласно кодировке Экспресс-3
#2000003 - код станции Москва(Казанский) согласно кодировке Экспресс-3

date = '2022-01-20'
station_from = '2024000'
station_to = '2000003'

params = {'apikey': key,
          'station': station_from,
          'transport_types' : 'train',
          'date' : date,
          'system' : 'express',
          'event' : 'departure',
          'direction' : station_to}

response = requests.get(url, params=params)
j_data = response.json()

print(f"По данному направлению следуют {j_data.get('pagination').get('total')} поездов")

with open('data.json', 'w') as f:
    json.dump(j_data, f)

