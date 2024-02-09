import json, os, requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import datetime
from collections import namedtuple

def km_formatter(x, pos):
    return f'{int(int(x)/1000000)}'

api_key = os.getenv("NASA_API_KEY")

start_date = "2024-02-08"
end_date = "2024-02-09"

url = "https://api.nasa.gov/neo/rest/v1/feed?" \
    f"start_date={start_date}&end_date={end_date}&api_key={api_key}"

response = requests.get(url)
data = response.json()


with open("asteroids.json", "w") as file:
    json.dump(data, file, indent=4)

with open("asteroids.json", "r") as file:
    data = json.load(file)

num_of_NEO = data["element_count"]
i = 0
# print(json.dumps(data["near_earth_objects"]["2024-02-09"][i], indent=4))
# print(data["near_earth_objects"]["2024-02-09"][i]["name"])
# print(data["near_earth_objects"]["2024-02-09"][i]["close_approach_data"][0]["close_approach_date_full"])
# print(data["near_earth_objects"]["2024-02-09"][i]["close_approach_data"][0]["miss_distance"]["kilometers"])

NEO = namedtuple('NEO', ['date', 'distance', 'name', 'id'])
neo_list = []
# new_todos = [item.strip("\n") for item in todos]
for i in data["near_earth_objects"]["2024-02-09"]: # co z tą datą???
    print(i["name"])
    neo_list.append(NEO(
        date=i["close_approach_data"][0]["close_approach_date_full"],
        distance=round(float(i["close_approach_data"][0]["miss_distance"]["kilometers"])),
        name=i["name"],
        id=i["id"]
        ))

for neo in neo_list:
    print(neo)

dates = [datetime.strptime(neo.date, "%Y-%b-%d %H:%M") for neo in neo_list]
distances = [neo.distance for neo in neo_list]
# labels = [f"{neo.name[1:-1]}, ({neo.id})" for neo in neo_list]
labels = [f"id: {neo.id} \nname: {neo.name}" for neo in neo_list]

fig, ax = plt.subplots()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.yaxis.set_major_formatter(FuncFormatter(km_formatter))
ax.scatter(dates, distances)

for i, label in enumerate(labels):
    ax.annotate(label, (dates[i], distances[i]), textcoords="offset points", xytext=(0, 10))


plt.xticks(rotation=45)
plt.xlabel('Data i godzina zbliżenia')
plt.ylabel('Odległość [mln km]')
plt.title('Odległość obiektu od Ziemi')
plt.tight_layout()
plt.show()

