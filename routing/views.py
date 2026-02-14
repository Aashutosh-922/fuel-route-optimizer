from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from .services import get_route
from .fuel_logic import compute_fuel_plan

class RouteFuelView(APIView):

    def get(self, request):
        start = request.GET.get("start")
        end = request.GET.get("end")

        if not start or not end:
            return Response(
                {"error": "start and end required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cache_key = f"{start}_{end}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        # For demo: hardcoded coords (replace with geocoding if needed)
        start_coords = [-104.9903, 39.7392]  # Denver
        end_coords = [-87.6298, 41.8781]     # Chicago

        route_data = get_route(start_coords, end_coords)

        stops, total_cost = compute_fuel_plan(route_data)

        result = {
            "route": route_data,
            "fuel_stops": stops,
            "total_fuel_cost": total_cost
        }

        cache.set(cache_key, result, 60 * 60)

        return Response(result)
