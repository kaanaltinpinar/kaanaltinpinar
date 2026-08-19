from flask import Flask, render_template, request, redirect, session, url_for
import math

app = Flask(__name__)
app.secret_key = "flight-ops-secret-2026"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

AIRPORTS = {
    "IST": {"name": "Istanbul Airport", "lat": 41.275, "lon": 28.751},
    "SAW": {"name": "Sabiha Gokcen", "lat": 40.898, "lon": 29.309},
    "ESB": {"name": "Ankara Esenboga", "lat": 40.128, "lon": 32.995},
    "ADB": {"name": "Izmir Adnan Menderes", "lat": 38.292, "lon": 27.157},
    "FRA": {"name": "Frankfurt", "lat": 50.037, "lon": 8.562},
    "LHR": {"name": "London Heathrow", "lat": 51.470, "lon": -0.461},
    "CDG": {"name": "Paris Charles de Gaulle", "lat": 49.009, "lon": 2.547},
    "AMS": {"name": "Amsterdam Schiphol", "lat": 52.309, "lon": 4.764},
    "DXB": {"name": "Dubai International", "lat": 25.253, "lon": 55.365}
}

AIRCRAFT = {
    "Airbus A320": {
        "cruise": 830,
        "fuel_capacity": 24210,
        "max_pax": 186,
        "callsign": "TK-A320"
    },
    "Airbus A321": {
        "cruise": 840,
        "fuel_capacity": 24200,
        "max_pax": 220,
        "callsign": "TK-A321"
    },
    "Boeing 737-800": {
        "cruise": 830,
        "fuel_capacity": 26020,
        "max_pax": 189,
        "callsign": "TK-B738"
    }
}


def calculate_distance(dep, dest):
    a = AIRPORTS[dep]
    b = AIRPORTS[dest]

    r = 6371

    lat1 = math.radians(a["lat"])
    lat2 = math.radians(b["lat"])

    dlat = math.radians(b["lat"] - a["lat"])
    dlon = math.radians(b["lon"] - a["lon"])

    x = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return round(r * 2 * math.asin(math.sqrt(x)))


def simulate(form):
    aircraft = form.get("aircraft", "Airbus A320")
    departure = form.get("departure", "IST")
    destination = form.get("destination", "FRA")

    passengers = int(form.get("passengers", 165))
    fuel = int(form.get("fuel", 18000))
    weather = form.get("weather", "moderate")

    ac = AIRCRAFT[aircraft]

    passengers = min(passengers, ac["max_pax"])

    dist = calculate_distance(departure, destination)

    weather_scores = {
        "normal": ("LOW", 10),
        "moderate": ("MEDIUM", 30),
        "poor": ("HIGH", 60),
        "severe": ("SEVERE", 90)
    }

    weather_risk, score = weather_scores.get(
        weather,
        ("LOW", 10)
    )

    fuel_required = round(
        dist * 2.65 + max(1500, dist * 0.35)
    )

    fuel_margin = fuel - fuel_required

    if fuel_margin < 0:
        score += 50
    elif fuel_margin < 1500:
        score += 20

    if score >= 75:
        decision = "NO-GO"
        recommendation = "Operational limits exceeded"
    elif score >= 40:
        decision = "CAUTION"
        recommendation = "Review before departure"
    else:
        decision = "GO"
        recommendation = "Within operational limits"

    if passengers >= ac["max_pax"] * 0.90:
        takeoff = "LIMITED"
    else:
        takeoff = "NORMAL"

    if weather in ["poor", "severe"]:
        landing = "CAUTION"
    else:
        landing = "NORMAL"

    alternates = {
        "FRA": "STR",
        "LHR": "CDG",
        "CDG": "ORY",
        "AMS": "BRU",
        "DXB": "AUH"
    }

    return {
        "aircraft": aircraft,
        "callsign": ac["callsign"],
        "departure": departure,
        "destination": destination,
        "departure_name": AIRPORTS[departure]["name"],
        "destination_name": AIRPORTS[destination]["name"],
        "passengers": passengers,
        "fuel": fuel,
        "fuel_required": fuel_required,
        "fuel_margin": fuel_margin,
        "distance": dist,
        "cruise_speed": ac["cruise"],
        "weather_risk": weather_risk,
        "crosswind_risk": "LOW",
        "notam_risk": "LOW",
        "alternate": alternates.get(destination, "SAW"),
        "takeoff": takeoff,
        "landing": landing,
        "decision": decision,
        "recommendation": recommendation
    }


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("index"))

        error = "Kullanici adi veya sifre hatali."

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    data = simulate({
        "aircraft": "Airbus A320",
        "departure": "IST",
        "destination": "FRA",
        "passengers": 165,
        "fuel": 18000,
        "weather": "moderate"
    })

    return render_template(
        "index.html",
        data=data,
        airports=AIRPORTS,
        aircraft=AIRCRAFT,
        username=session.get("username")
    )


@app.route("/simulate", methods=["POST"])
def run_simulation():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    data = simulate(request.form)

    return render_template(
        "index.html",
        data=data,
        airports=AIRPORTS,
        aircraft=AIRCRAFT,
        username=session.get("username")
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)