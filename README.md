# Fuel Route Optimizer API

A Django REST API that calculates the most cost-effective fuel stops along a driving route in the United States.

The API determines:
- The driving route between two locations
- Optimal refueling points based on fuel prices dataset
- Total fuel cost for the trip

The system is optimized for performance and minimizes external API calls.

---

## 🚀 Features

- Uses **OpenRouteService** for route calculation (single external call)
- Computes fuel stops locally using provided fuel price dataset
- Handles long routes with multiple refueling points
- Calculates total trip fuel cost using vehicle mileage
- Caches results to improve response time
- Works entirely offline after route retrieval

---

## ⚙️ Assumptions

| Parameter | Value |
|--------|------|
Vehicle Range | 500 miles per full tank
Fuel Efficiency | 10 miles per gallon
Optimization Goal | Minimum fuel cost
Geographic Scope | USA only

---

## 🧠 Optimization Strategy

The dataset contains fuel prices by **city/state (not coordinates)**.

Therefore instead of spatial station matching, the problem is modeled as a:

> **Minimum Cost Refueling Problem**

Steps:

1. Fetch route geometry (single API call)
2. Sample route at intervals (~100 miles)
3. Map sampled points to nearest cities in dataset
4. Choose cheapest reachable fuel city before tank runs low
5. Simulate travel and refueling
6. Compute total cost

This avoids multiple map API calls and keeps response fast.

---

## 📡 API Endpoint

https://www.loom.com/share/d067e7df775e4d198d434caeecb98d81
