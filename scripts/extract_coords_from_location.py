import os
import csv
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.extra.rate_limiter import RateLimiter

# Setup geolocator and rate limiter
geolocator = Nominatim(user_agent="geoapi")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def fetch_coordinates(location, index):
    try:
        loc = geocode(location)
        if not loc: return None

        print(f"Processed location #{index}: {location} with coordinates ({loc.latitude}, {loc.longitude})")
        return loc.latitude, loc.longitude
    except (GeocoderTimedOut, GeocoderUnavailable):
        print(f"Timeout or unavailable error for location #{index}: {location}")
    except Exception as e:
        print(f"Cannot geocode location #{index}: {location}.")
    
    return None


def save_to_csv(data, filename="../data/extracted/locations_coordinates.csv"):
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        for location, lat, lng, count in data:
            writer.writerow([location, lat, lng, count])


if __name__ == "__main__":
    file_path = os.path.join("..", "data", "extracted", "reviews.csv")

    df = pd.read_csv(file_path)
    location_counts = df["location"].value_counts()

    results = []  # To store (location, lat, lon, count) tuples
    for index, (location, count) in enumerate(location_counts.items(), 1):
        coords = fetch_coordinates(location, index)
        if coords:
            lat, lng = coords
            results.append((location, lat, lng, count))
        
        # Save every 100 geocoded locations
        if index % 100 == 0:
            save_to_csv(results)
            results = []

    # Save the remaining data if any
    if results:
        save_to_csv(results)

    print("Geocoding completed.")
