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

GET /api/route/?start=<city>&end=<city>


### Example



GET /api/route/?start=Denver&end=Chicago


### Response

```json
{
  "fuel_stops": [
    {
      "city": "Omaha",
      "state": "NE",
      "price": 3.20,
      "gallons": 42.5,
      "cost": 136.0
    }
  ],
  "total_fuel_cost": 136.0
}

🏗️ Project Structure
fuel_optimizer/
│
├── config/              # Django settings
├── routing/
│   ├── views.py         # API layer
│   ├── services.py      # External routing API call
│   ├── fuel_logic.py    # Optimization algorithm
│
├── data/
│   └── fuel-prices-for-be-assessment.csv
│
├── manage.py
└── requirements.txt

🔌 External Dependency

OpenRouteService Directions API

Only one request per route is made.

All fuel optimization is local.

🛠️ Setup Instructions
1. Clone repo
git clone https://github.com/<username>/fuel-route-optimizer.git
cd fuel-route-optimizer

2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Add environment variables

Create .env

ORS_API_KEY=your_api_key_here

5. Run server
python manage.py runserver

🧪 Testing

Open in browser or Postman:

http://127.0.0.1:8000/api/route/?start=Denver&end=Chicago

⚡ Performance Considerations

Only one routing API call

Fuel dataset loaded once into memory

No repeated file reads

Cached responses

Linear traversal algorithm

🎥 Demo

Loom video: https://www.loom.com/share/d067e7df775e4d198d434caeecb98d81

📌 Future Improvements

Live fuel price integration

Proper geocoding for city coordinates

Redis caching

Multiple vehicle profiles

EV charging support

👨‍💻 Author

Aashutosh Karale
