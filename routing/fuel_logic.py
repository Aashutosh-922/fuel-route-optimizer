import os
import csv
import math
from collections import defaultdict
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "fuel-prices-for-be-assessment.csv")

def haversine(lat1, lon1, lat2, lon2):
    R = 3959  # miles
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def load_city_prices():
    city_prices = defaultdict(lambda: float('inf'))

    with open(DATA_FILE, newline='', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        for row in reader:
            try:
                city = row["City"].strip()
                state = row["State"].strip()
                price = float(row["Retail Price"].strip())

                key = (city, state)
                city_prices[key] = min(city_prices[key], price)

            except Exception:
                continue

    return dict(city_prices)


CITY_PRICES = load_city_prices()
CITY_COORDS = {}


def compute_fuel_plan(route_geojson):
    coords = route_geojson["features"][0]["geometry"]["coordinates"]
    sampled = sample_route_points(coords)

    # Build pseudo city coordinates along route
    for point in sampled:
        lat, lon = point[1], point[0]

        for (city, state) in CITY_PRICES.keys():
            if (city, state) not in CITY_COORDS:
                CITY_COORDS[(city, state)] = (lat, lon)

    stops = []
    fuel_left = 500
    total_cost = 0

    for i in range(len(sampled) - 1):

        dist = haversine(
            sampled[i][1], sampled[i][0],
            sampled[i+1][1], sampled[i+1][0]
        )

        fuel_left -= dist

        if fuel_left <= 100:
            city = nearest_city(sampled[i][1], sampled[i][0])

            if city in CITY_PRICES:
                gallons = (500 - fuel_left) / settings.MPG
                price = CITY_PRICES[city]
                cost = gallons * price

                stops.append({
                    "city": city[0],
                    "state": city[1],
                    "price": round(price, 3),
                    "gallons": round(gallons, 2),
                    "cost": round(cost, 2)
                })

                total_cost += cost
                fuel_left = 500

    return stops, round(total_cost, 2)

def sample_route_points(coords, step=160000):  # ~100 miles
    sampled = [coords[0]]
    distance_acc = 0

    for i in range(1, len(coords)):
        distance_acc += haversine(
            coords[i-1][1], coords[i-1][0],
            coords[i][1], coords[i][0]
        ) * 1609

        if distance_acc >= step:
            sampled.append(coords[i])
            distance_acc = 0

    sampled.append(coords[-1])
    return sampled

def nearest_city(lat, lon):
    best_city = None
    best_dist = float('inf')

    for (city, state), (clat, clon) in CITY_COORDS.items():
        d = haversine(lat, lon, clat, clon)
        if d < best_dist:
            best_dist = d
            best_city = (city, state)

    return best_city


