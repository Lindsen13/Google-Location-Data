import json
import datetime
import pandas as pd

with open('Location History.json') as json_file:
    data = json.load(json_file)

output_json = []
for loc in data.get('locations'):
    output_json.append({
        'timestamp':datetime.datetime.fromtimestamp(int(loc.get('timestampMs'))/1000),
        'latitude':loc.get('latitudeE7') / 10**7,
        'longitude':loc.get('longitudeE7') / 10**7
        })

df = pd.DataFrame(data = output_json)

df.to_csv('output.csv',index=False)
