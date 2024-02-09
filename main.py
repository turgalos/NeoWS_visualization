import json, os, requests
import plotly.express as px
from datetime import datetime
from collections import namedtuple
import pandas as pd


api_key = os.getenv("NASA_API_KEY")
start_date = "2024-02-09"
end_date = "2024-02-11"

url = 'https://api.nasa.gov/neo/rest/v1/feed?' \
      f'start_date={start_date}&end_date={end_date}&api_key={api_key}'

response = requests.get(url)
data = response.json()

with open("asteroids.json", "w") as file:
    json.dump(data, file, indent=4)

with open("asteroids.json", "r") as file:
    data = json.load(file)

num_of_NEO = data["element_count"]
NEO = namedtuple('NEO', ['date', 'distance', 'name', 'id'])
neo_list = []

for j in data["near_earth_objects"]:
    for i in data["near_earth_objects"][j]:
        neo_list.append(NEO(
            date=i["close_approach_data"][0]["close_approach_date_full"],
            distance=round(float(i["close_approach_data"][0]["miss_distance"]["kilometers"])),
            name=i["name"],
            id=i["id"]
        ))

# for neo in neo_list:
#     print(neo)

dates = [datetime.strptime(neo.date, "%Y-%b-%d %H:%M") for neo in neo_list]
distances = [neo.distance for neo in neo_list]
labels = [f"id: {neo.id} | name: {neo.name}" for neo in neo_list]

df = pd.DataFrame({
    'Date': [neo.date for neo in neo_list],
    'Distance': [neo.distance for neo in neo_list],
    'Name & ID': [f"{neo.name} | {neo.id}" for neo in neo_list]
})

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%b-%d %H:%M')
fig = px.scatter(df, x='Date', y='Distance', text='Name & ID', title='Obiekty w przestrzeni okołoziemskiej:')
fig.update_yaxes(tickprefix="", ticksuffix=" km")
fig.update_traces(mode='markers+text', textposition='top center', marker=dict(size=5), hoverinfo='text')

fig.show()