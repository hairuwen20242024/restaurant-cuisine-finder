import requests
import googlemaps
import csv
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

def get_location_from_ip():
    response = requests.get('https://ipinfo.io')
    data = response.json()
    loc = data['loc'].split(',')
    lat = float(loc[0])
    lng = float(loc[1])
    return lat, lng

def get_restaurants(api_key, lat, lng, radius):
    gmaps = googlemaps.Client(key=api_key)
    places_result = gmaps.places_nearby(location=(lat, lng), radius=radius, type='restaurant')
    return places_result['results']

def save_to_csv(data, filename='restaurants_IP.csv'):
    # Extract all field names
    all_keys = set()
    for item in data:
        all_keys.update(item.keys())
    all_keys = list(all_keys)
    
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=all_keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python getUserLocationAndNearbyRestaurants.py <radius_in_miles>")
        sys.exit(1)

    radius_miles = float(sys.argv[1])
    radius_meters = radius_miles * 1609.34  # Convert miles to meters

    # api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
    api_key = 'AIzaSyDl9CWJ-7gFEqrgNLHh_i1EVRD6RohEPbw' 
    lat, lng = get_location_from_ip()
    logging.debug(f'Lat: {lat}, Lng: {lng}')
    restaurants = get_restaurants(api_key, lat, lng, radius_meters)
    logging.debug(f'Restaurants fetched: {len(restaurants)}')
    save_to_csv(restaurants)
    # print("Restaurants data fetched and saved to restaurants_IP.csv")
    logging.debug("Restaurants data fetched and saved to data/restaurants_IP.csv")
