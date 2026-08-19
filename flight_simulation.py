from data.notams import NOTAMS
from data.airports import ALTERNATE_AIRPORTS
from data.weather import WEATHER 
from data.performance import AIRCRAFT_PERFORMANCE
import math
import time
AIRPORTS = {
    "IST": {
        "name": "Istanbul Airport",
        "latitude": 41.2753,
        "longitude": 28.7519
    },
    "FRA": {
        "name": "Frankfurt Airport",
        "latitude": 50.0379,
        "longitude": 8.5622
    }
}

AIRCRAFT = {
    "A320": {
        "name": "Airbus A320",
        "cruise_speed": 840,
        "fuel_burn": 2500,
        "max_passengers": 180
    },
    "B737": {
        "name": "Boeing 737-800",
        "cruise_speed": 842,
        "fuel_burn": 2450,
        "max_passengers": 189
    }
}


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def show_phase(phase, altitude, speed, fuel, status):
    print()
    print("--------------------------------")
    print(f"PHASE: {phase}")
    print("--------------------------------")
    print(f"Altitude : {altitude:,} ft")
    print(f"Speed    : {speed} kt")
    print(f"Fuel     : {fuel:,.0f} kg")
    print(f"Status   : {status}")
    print("--------------------------------")

    time.sleep(1)


print("================================")
print("      FLIGHTOPS SIMULATOR")
print("================================")

print("\nAircraft:")
print("1 - Airbus A320")
print("2 - Boeing 737-800")

choice = input("\nSelect aircraft (1/2): ")

if choice == "1":
    aircraft = AIRCRAFT["A320"]
elif choice == "2":
    aircraft = AIRCRAFT["B737"]
else:
    print("Invalid aircraft selection.")
    exit()

passengers = int(input("Number of passengers: "))

if passengers > aircraft["max_passengers"]:
    print("ERROR: Passenger count exceeds aircraft capacity.")
    exit()

distance = calculate_distance(
    AIRPORTS["IST"]["latitude"],
    AIRPORTS["IST"]["longitude"],
    AIRPORTS["FRA"]["latitude"],
    AIRPORTS["FRA"]["longitude"]
)

flight_time = distance / aircraft["cruise_speed"]
fuel_required = flight_time * aircraft["fuel_burn"]

# Yak�t rezervi
reserve_fuel = fuel_required * 0.15
total_fuel = fuel_required + reserve_fuel

print("\n================================")
print("          FLIGHT PLAN")
print("================================")
print(f"Aircraft       : {aircraft['name']}")
print("Route          : IST -> FRA")
print(f"Passengers     : {passengers}")
print(f"Distance       : {distance:.0f} km")
print(f"Cruise Speed   : {aircraft['cruise_speed']} km/h")
print(f"Flight Time    : {flight_time:.2f} hours")
print(f"Trip Fuel      : {fuel_required:.0f} kg")
print(f"Reserve Fuel   : {reserve_fuel:.0f} kg")
print(f"Total Fuel     : {total_fuel:.0f} kg")
print("================================")

input("\nPress ENTER to start flight...")

fuel = total_fuel

# 1 - PRE-FLIGHT
show_phase(
    "PRE-FLIGHT",
    0,
    0,
    fuel,
    "READY"
)

# 2 - TAXI
fuel -= 150

show_phase(
    "TAXI",
    0,
    15,
    fuel,
    "TAXIING TO RUNWAY"
)

# 3 - TAKEOFF
fuel -= 300

show_phase(
    "TAKEOFF",
    2500,
    180,
    fuel,
    "AIRBORNE"
)

# 4 - CLIMB
fuel -= 600

show_phase(
    "CLIMB",
    30000,
    280,
    fuel,
    "CLIMBING"
)

# 5 - CRUISE
cruise_fuel = fuel - fuel_required * 0.45

show_phase(
    "CRUISE",
    36000,
    450,
    cruise_fuel,
    "CRUISE"
)

# 6 - DESCENT
fuel = cruise_fuel - 500

show_phase(
    "DESCENT",
    18000,
    300,
    fuel,
    "DESCENDING"
)

# 7 - APPROACH
fuel -= 300

show_phase(
    "APPROACH",
    3000,
    160,
    fuel,
    "FINAL APPROACH"
)

# 8 - LANDING
fuel -= 200

show_phase(
    "LANDING",
    0,
    0,
    fuel,
    "LANDED"
)

print()
print("================================")
print("       FLIGHT COMPLETED")
print("================================")
print("Route  : IST -> FRA")
print(f"Aircraft: {aircraft['name']}")
print(f"Passengers: {passengers}")
print(f"Remaining Fuel: {fuel:,.0f} kg")
print("Status : SUCCESS")
print("================================")
def calculate_weather_risk(weather):
    risk = 0

    if weather["visibility"] < 5000:
        risk += 2
    elif weather["visibility"] < 8000:
        risk += 1

    if weather["ceiling"] < 1000:
        risk += 2
    elif weather["ceiling"] < 2000:
        risk += 1

    if weather["weather"] == "RAIN":
        risk += 1

    if risk >= 4:
        return "HIGH"
    elif risk >= 2:
        return "MEDIUM"
    else:
        return "LOW"
arrival_weather = WEATHER["FRA"]

weather_risk = calculate_weather_risk(arrival_weather)

print("================================")
print("       WEATHER RISK")
print("================================")
print(f"Arrival Airport : FRA")
print(f"Weather         : {arrival_weather['weather']}")
print(f"Visibility      : {arrival_weather['visibility']} m")
print(f"Ceiling         : {arrival_weather['ceiling']} ft")
print(f"Risk Level      : {weather_risk}")
if weather_risk == "HIGH":
    print("?? WEATHER WARNING")
    print("Flight operation requires additional assessment.")

elif weather_risk == "MEDIUM":
    print("?? WEATHER CAUTION")
    print("Additional operational attention required.")

else:
    print("? WEATHER STATUS: NORMAL")
print("================================")
def show_performance(aircraft):
    print("================================")
    print("       FLIGHT PERFORMANCE")
    print("================================")
    print(f"Aircraft          : {aircraft['name']}")
    print(f"Cruise Speed      : {aircraft['cruise_speed']} km/h")
    print(f"Fuel Burn         : {aircraft['fuel_burn']} kg/h")
    print(f"Max Passengers    : {aircraft['max_passengers']}")
    print("Performance       : NORMAL")
    print("================================")


show_performance(aircraft)
def calculate_wind_effect(wind_direction, wind_speed, runway_direction):
    angle = abs(wind_direction - runway_direction)

    if angle > 180:
        angle = 360 - angle

    import math

    headwind = wind_speed * math.cos(math.radians(angle))
    crosswind = wind_speed * math.sin(math.radians(angle))

    return headwind, crosswind


# FRA runway direction
runway_direction = 240

headwind, crosswind = calculate_wind_effect(
    240,
    12,
    runway_direction
)

print("================================")
print("          WIND ANALYSIS")
print("================================")
print(f"Wind Direction : 240�")
print(f"Wind Speed     : 12 kt")
print(f"Headwind       : {headwind:.1f} kt")
print(f"Crosswind      : {crosswind:.1f} kt")
print("================================")
def assess_crosswind(crosswind, max_crosswind):
    if crosswind <= max_crosswind * 0.5:
        return "LOW"

    elif crosswind <= max_crosswind * 0.75:
        return "MEDIUM"

    else:
        return "HIGH"


max_crosswind = 38

crosswind_risk = assess_crosswind(
    crosswind,
    max_crosswind
)

print("================================")
print("       CROSSWIND RISK")
print("================================")
print(f"Crosswind       : {crosswind:.1f} kt")
print(f"Aircraft Limit  : {max_crosswind} kt")
print(f"Risk Level      : {crosswind_risk}")

if crosswind_risk == "LOW":
    print("Status          : NORMAL OPERATIONS")

elif crosswind_risk == "MEDIUM":
    print("?? Status       : CAUTION")

else:
    print("?? Status        : HIGH CROSSWIND")
    print("Operational assessment required.")

print("================================")
def assess_crosswind(crosswind, max_crosswind):
    if crosswind <= max_crosswind * 0.5:
        return "LOW"
    elif crosswind <= max_crosswind * 0.75:
        return "MEDIUM"
    else:
        return "HIGH"


max_crosswind = 38

crosswind_risk = assess_crosswind(
    crosswind,
    max_crosswind
)

print("================================")
print("       CROSSWIND RISK")
print("================================")
print(f"Crosswind       : {crosswind:.1f} kt")
print(f"Aircraft Limit  : {max_crosswind} kt")
print(f"Risk Level      : {crosswind_risk}")

if crosswind_risk == "LOW":
    print("Status          : NORMAL OPERATIONS")
elif crosswind_risk == "MEDIUM":
    print("?? Status       : CAUTION")
else:
    print("?? Status        : HIGH CROSSWIND")
    print("Operational assessment required.")


def select_alternate(destination):
    alternates = ALTERNATE_AIRPORTS.get(destination, [])

    print("================================")
    print("       ALTERNATE AIRPORT")
    print("================================")

    best = None

    for airport in alternates:
        print(f"Alternate        : {airport['icao']}")
        print(f"Distance         : {airport['distance']} km")
        print(f"Weather          : {airport['weather']}")
        print(f"Risk Level       : {airport['risk']}")
        print("--------------------------------")

        if airport["risk"] == "LOW":
            if best is None or airport["distance"] < best["distance"]:
                best = airport

    print()

    if best:
        print(f"Recommended      : {best['icao']}")
        print("Reason           : Lowest distance with LOW risk")
        selected_alternate = best["icao"]
    else:
        print("Recommended      : NONE")
        print("Reason           : No suitable alternate found")
        selected_alternate = "NONE"

    print("================================")

    return selected_alternate

alternate = select_alternate("FRA")

def show_notams(airport):
    highest_risk = "LOW"
    notams = NOTAMS.get(airport, [])

    print("================================")
    print("          NOTAM CHECK")
    print("================================")
    print(f"Airport          : {airport}")
    return highest_risk

    if not notams:
        print("No active NOTAM found.")
        print("Operational Risk : LOW")
        print("================================")
        return 

    for i, notam in enumerate(notams, 1):
        print()
        print(f"NOTAM {i}")
        print(f"ID               : {notam['id']}")
        print(f"Description      : {notam['description']}")
        print(f"Status           : {notam['status']}")
        print(f"Impact           : {notam['impact']}")

        if notam["impact"] == "HIGH":
            highest_risk = "HIGH"
        elif notam["impact"] == "MEDIUM" and highest_risk == "LOW":
            highest_risk = "MEDIUM"

    print()
    print(f"Operational Risk : {highest_risk}")

    if highest_risk == "HIGH":
        print("?? ATTENTION REQUIRED")
    elif highest_risk == "MEDIUM":
        print("?? OPERATIONAL CAUTION")
    else:
        print("NORMAL OPERATIONS")

    print("================================")
    return highest_risk


notam_risk = show_notams("FRA")

def operational_decision(
 
    weather_risk,
    crosswind_risk,
    notam_risk,
    alternate
):
    print("================================")
    print("      OPERATIONAL DECISION")
    print("================================")

    print(f"Weather Risk     : {weather_risk}")
    print(f"Crosswind Risk   : {crosswind_risk}")
    print(f"NOTAM Risk       : {notam_risk}")
    print(f"Alternate        : {alternate}")

    print("--------------------------------")
    print("FINAL ASSESSMENT")
    print("--------------------------------")

    if notam_risk == "HIGH":
        decision = "CAUTION"
        recommendation = "REVIEW BEFORE DEPARTURE"

    elif weather_risk == "HIGH":
        decision = "CAUTION"
        recommendation = "REVIEW WEATHER CONDITIONS"

    elif crosswind_risk == "HIGH":
        decision = "CAUTION"
        recommendation = "REVIEW CROSSWIND LIMITS"

    else:
        decision = "GO"
        recommendation = "NORMAL OPERATIONS"

    print(f"Decision         : {decision}")
    print(f"Recommendation   : {recommendation}")

    print("================================")
    return weather_risk
    print("================================")
    print("       AUTOMATIC OPS CHECK")
    print("================================")
operational_decision(
    weather_risk,
    crosswind_risk,
    "HIGH",
    "STR"
)
print("================================")
print("   AUTOMATED OPERATIONAL DECISION")
print("================================")

operational_decision(
    weather_risk,
    crosswind_risk,
    notam_risk,
    alternate
)

def show_flight_plan(aircraft, passengers, distance):
    cruise_speed = aircraft["cruise_speed"]

    flight_time = distance / cruise_speed

    trip_fuel = flight_time * aircraft["fuel_burn"]
    reserve_fuel = trip_fuel * 0.15
    total_fuel = trip_fuel + reserve_fuel

    print("================================")
    print("          FLIGHT PLAN")
    print("================================")
    print(f"Departure        : IST")
    print(f"Arrival          : FRA")
    print(f"Aircraft         : {aircraft['name']}")
    print(f"Passengers       : {passengers}")
    print(f"Distance         : {distance:.0f} km")
    print(f"Cruise Speed     : {cruise_speed} km/h")
    print(f"Flight Time      : {flight_time:.2f} hours")
    print(f"Trip Fuel        : {trip_fuel:,.0f} kg")
    print(f"Reserve Fuel     : {reserve_fuel:,.0f} kg")
    print(f"Total Fuel       : {total_fuel:,.0f} kg")
    print("================================")
show_flight_plan(aircraft, passengers, distance)

def show_takeoff_performance(aircraft, passengers, fuel):
    max_passengers = aircraft["max_passengers"]
    passenger_load = (passengers / max_passengers) * 100

    if passenger_load < 70:
        performance = "GOOD"
    elif passenger_load < 90:
        performance = "NORMAL"
    else:
        performance = "LIMITED"

    print("================================")
    print("       TAKEOFF PERFORMANCE")
    print("================================")
    print(f"Aircraft          : {aircraft['name']}")
    print(f"Passengers        : {passengers}")
    print(f"Passenger Load    : {passenger_load:.1f}%")
    print(f"Fuel              : {fuel:,.0f} kg")
    print(f"Performance       : {performance}")
    print("================================")

    return performance

def show_landing_performance(aircraft, passengers, fuel, weather_risk):
    max_passengers = aircraft["max_passengers"]
    passenger_load = (passengers / max_passengers) * 100

    if weather_risk == "HIGH":
        performance = "LIMITED"
    elif weather_risk == "MEDIUM":
        performance = "CAUTION"
    else:
        performance = "NORMAL"

    print("================================")
    print("       LANDING PERFORMANCE")
    print("================================")
    print(f"Aircraft          : {aircraft['name']}")
    print(f"Passengers        : {passengers}")
    print(f"Passenger Load    : {passenger_load:.1f}%")
    print(f"Landing Fuel      : {fuel:,.0f} kg")
    print(f"Weather Risk      : {weather_risk}")
    print(f"Performance       : {performance}")
    print("================================")

    return performance


takeoff_performance = show_takeoff_performance(
    aircraft,
    passengers,
    fuel
)

takeoff_performance = show_takeoff_performance(
    aircraft,
    passengers,
    fuel
)

landing_performance = show_landing_performance(
    aircraft,
    passengers,
    fuel,
    weather_risk
)
def final_dispatch_report(
    aircraft,
    passengers,
    weather_risk,
    crosswind_risk,
    notam_risk,
    alternate,
    takeoff_performance,
    landing_performance
):
    risks = [
        weather_risk,
        crosswind_risk,
        notam_risk
    ]

    if "HIGH" in risks or landing_performance == "LIMITED":
        decision = "NO-GO"
        recommendation = "DO NOT DEPART"
    elif "MEDIUM" in risks or landing_performance == "CAUTION":
        decision = "CAUTION"
        recommendation = "REVIEW BEFORE DEPARTURE"
    else:
        decision = "GO"
        recommendation = "NORMAL OPERATIONS"

    print("========================================")
    print("          FINAL DISPATCH REPORT")
    print("========================================")
    print(f"Aircraft           : {aircraft['name']}")
    print(f"Passengers         : {passengers}")
    print("----------------------------------------")
    print(f"Weather Risk       : {weather_risk}")
    print(f"Crosswind Risk     : {crosswind_risk}")
    print(f"NOTAM Risk         : {notam_risk}")
    print(f"Alternate          : {alternate}")
    print(f"Takeoff Performance: {takeoff_performance}")
    print(f"Landing Performance: {landing_performance}")
    print("----------------------------------------")
    print("FINAL DECISION")
    print("----------------------------------------")
    print(f"Decision           : {decision}")
    print(f"Recommendation     : {recommendation}")
    print("========================================")

final_dispatch_report(
    aircraft,
    passengers,
    weather_risk,
    crosswind_risk,
    notam_risk,
    alternate,
    takeoff_performance,
    landing_performance
)

def in_flight_monitor(aircraft, fuel, altitude, speed, flight_time):
    fuel_burn = aircraft["fuel_burn"]

    fuel_used = fuel_burn * flight_time
    remaining_fuel = fuel - fuel_used

    if remaining_fuel < 1000:
        fuel_status = "CRITICAL"
    elif remaining_fuel < 1500:
        fuel_status = "LOW"
    else:
        fuel_status = "NORMAL"

    if altitude < 10000:
        phase = "CLIMB"
    elif flight_time > 1:
        phase = "CRUISE"
    else:
        phase = "CLIMB"

    print("================================")
    print("       IN-FLIGHT MONITORING")
    print("================================")
    print(f"Flight Phase      : {phase}")
    print(f"Altitude          : {altitude:,.0f} ft")
    print(f"Speed             : {speed} km/h")
    print(f"Fuel Used         : {fuel_used:,.0f} kg")
    print(f"Remaining Fuel    : {remaining_fuel:,.0f} kg")
    print(f"Fuel Status       : {fuel_status}")
    print("================================")

    return remaining_fuel
    in_flight_monitor(
    aircraft,
    fuel,
    30000,
    830,
    flight_time
)
def flight_progress(distance, cruise_speed, flight_time, fuel, fuel_burn):
    total_time = distance / cruise_speed
    remaining_time = max(total_time - flight_time, 0)

    progress = min((flight_time / total_time) * 100, 100)

    arrival_fuel = fuel - (fuel_burn * remaining_time)

    if arrival_fuel < 1000:
        fuel_status = "CRITICAL"
    elif arrival_fuel < 1500:
        fuel_status = "LOW"
    else:
        fuel_status = "NORMAL"

    print("================================")
    print("        FLIGHT PROGRESS")
    print("================================")
    print(f"Total Flight Time : {total_time:.2f} h")
    print(f"Elapsed Time      : {flight_time:.2f} h")
    print(f"Remaining Time    : {remaining_time:.2f} h")
    print(f"Progress          : {progress:.1f}%")
    print(f"Estimated Arrival : {remaining_time:.2f} h")
    print(f"Arrival Fuel      : {arrival_fuel:,.0f} kg")
    print(f"Fuel Status       : {fuel_status}")
    print("================================")

    return arrival_fuel

# FLIGHT PROGRESS
if "cruise_speed" in aircraft:
    current_cruise_speed = aircraft["cruise_speed"]
elif "cruise_speed_kmh" in aircraft:
    current_cruise_speed = aircraft["cruise_speed_kmh"]
else:
    current_cruise_speed = 830

arrival_fuel = flight_progress(
    distance,
    current_cruise_speed,
    flight_time,
    fuel,
    aircraft["fuel_burn"]
)
def show_operations_dashboard(
    aircraft,
    passengers,
    weather_risk,
    crosswind_risk,
    notam_risk,
    alternate,
    fuel,
    flight_time
):
    max_passengers = aircraft["max_passengers"]
    passenger_load = (passengers / max_passengers) * 100

    print()
    print("========================================")
    print("         OPERATIONS DASHBOARD")
    print("========================================")
    print(f"Route              : IST -> FRA")
    print(f"Aircraft            : {aircraft['name']}")
    print(f"Passengers          : {passengers}")
    print(f"Passenger Load      : {passenger_load:.1f}%")
    print("----------------------------------------")
    print(f"Weather Risk        : {weather_risk}")
    print(f"Crosswind Risk      : {crosswind_risk}")
    print(f"NOTAM Risk          : {notam_risk}")
    print(f"Alternate            : {alternate}")
    print("----------------------------------------")
    print(f"Remaining Fuel      : {fuel:,.0f} kg")
    print(f"Flight Time         : {flight_time:.2f} h")
    print("----------------------------------------")

    if "HIGH" in [weather_risk, crosswind_risk, notam_risk]:
        status = "HIGH OPERATIONAL RISK"
    elif "MEDIUM" in [weather_risk, crosswind_risk, notam_risk]:
        status = "OPERATIONAL CAUTION"
    else:
        status = "NORMAL OPERATIONS"

    print(f"Overall Status      : {status}")
    print("========================================")


show_operations_dashboard(
    aircraft,
    passengers,
    weather_risk,
    crosswind_risk,
    notam_risk,
    alternate,
    fuel,
    flight_time
)