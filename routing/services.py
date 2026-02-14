import requests
from django.conf import settings


def get_route(start_coords, end_coords):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

    response = requests.post(
        url,
        json={"coordinates": [start_coords, end_coords]},
        headers={
            "Authorization": settings.ORS_API_KEY,
            "Content-Type": "application/json"
        },
        timeout=5
    )

    response.raise_for_status()
    return response.json()
