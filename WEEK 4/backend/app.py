# # # OpenAI Integration with flask
# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import openai
# # import pandas as pd

# # app = Flask(__name__)
# # CORS(app)


# # # Load the restaurant data
# # df = pd.read_csv('cleaned_restaurants.csv')

# # def generate_response(prompt):
# #     response = openai.Completion.create(
# #         engine="text-davinci-003",
# #         prompt=prompt,
# #         max_tokens=150
# #     )
# #     return response.choices[0].text.strip()

# # def rag_pipeline(query, dataframe):
# #     relevant_data = dataframe[dataframe['name'].str.contains(query, case=False, na=False)]
# #     context = relevant_data.to_string(index=False)
# #     prompt = f"Answer the following question based on the context: {context}\n\nQuestion: {query}\nAnswer:"
# #     return generate_response(prompt)

# # @app.route('/search', methods=['POST'])
# # def search():
# #     query = request.json.get('query')
# #     response = rag_pipeline(query, df)
# #     return jsonify(response)

# # if __name__ == '__main__':
# #     app.run(debug=True)




# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import openai
# import pandas as pd
# import requests
# import googlemaps
# import csv

# app = Flask(__name__)
# CORS(app)

# API Keys
# GOOGLE_MAPS_API_KEY = 'MY_GOOGLE_MAPS_API_KEY'
# openai.api_key = 'MY_OPENAI_API_KEY'



# # Load the restaurant data
# df = pd.read_csv('cleaned_restaurants.csv')

# def get_location_from_ip():
#     response = requests.get('https://ipinfo.io')
#     data = response.json()
#     loc = data['loc'].split(',')
#     lat = float(loc[0])
#     lng = float(loc[1])
#     return lat, lng

# def get_restaurants(api_key, lat, lng, radius):
#     gmaps = googlemaps.Client(key=api_key)
#     places_result = gmaps.places_nearby(location=(lat, lng), radius=radius, type='restaurant')
#     return places_result['results']

# def save_to_csv(data, filename='restaurants_IP.csv'):
#     # Extract all field names
#     all_keys = set()
#     for item in data:
#         all_keys.update(item.keys())
#     all_keys = list(all_keys)
    
#     with open(filename, 'w', newline='', encoding='utf-8') as output_file:
#         dict_writer = csv.DictWriter(output_file, fieldnames=all_keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(data)

# @app.route('/get_location', methods=['POST'])
# def get_location():
#     lat, lng = get_location_from_ip()
#     return jsonify({'lat': lat, 'lon': lng}), 200

# @app.route('/get_restaurants', methods=['POST'])
# def fetch_restaurants():
#     data = request.get_json()
#     lat = data.get('lat')
#     lon = data.get('lon')
#     radius = data.get('radius')  # Radius in miles

#     if not all([lat, lon, radius]):
#         return jsonify({'error': 'Missing data'}), 400

#     radius_meters = radius * 1609.34  # Convert miles to meters

#     restaurants = get_restaurants(GOOGLE_MAPS_API_KEY, lat, lon, radius_meters)
#     save_to_csv(restaurants)
#     return jsonify(restaurants), 200

# def generate_response(prompt):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150
#     )
#     return response.choices[0].text.strip()

# def rag_pipeline(query, dataframe):
#     relevant_data = dataframe[dataframe['name'].str.contains(query, case=False, na=False)]
#     context = relevant_data.to_string(index=False)
#     prompt = f"Answer the following question based on the context: {context}\n\nQuestion: {query}\nAnswer:"
#     return generate_response(prompt)

# @app.route('/search', methods=['POST'])
# def search():
#     query = request.json.get('query')
#     response = rag_pipeline(query, df)
#     return jsonify(response)

# if __name__ == '__main__':
#     app.run(debug=True)






from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import pandas as pd
import subprocess
import logging

app = Flask(__name__)
CORS(app)

# API Keys
GOOGLE_MAPS_API_KEY = 'MY_GOOGLE_MAPS_API_KEY'
openai.api_key = 'MY_OPENAI_API_KEY'



logging.basicConfig(level=logging.DEBUG)

def run_script(script_name, args=[]):
    result = subprocess.run(["python", script_name] + args, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()

@app.route('/get_location_and_restaurants', methods=['POST'])
def get_location_and_restaurants():
    data = request.get_json()
    radius = data.get('radius')  # Radius in miles

    app.logger.debug(f'Received radius: {radius}')

    if not radius:
        return jsonify({'error': 'Missing radius'}), 400

    try:
        output = run_script("getUserLocationAndNearbyRestaurants.py", [str(radius)])
        app.logger.debug(f'getUserLocationAndNearbyRestaurants.py output: {output}')
        output = run_script("data_preprocessing.py")
        app.logger.debug(f'data_preprocessing.py output: {output}')
    except RuntimeError as e:
        app.logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Restaurants data fetched and preprocessed successfully'}), 200

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    app.logger.debug(f'Received query: {query}')
    try:
        df = pd.read_csv('data/cleaned_restaurants.csv')
    except FileNotFoundError:
        app.logger.error('Data file not found')
        return jsonify({'error': 'Data file not found'}), 500
    response = rag_pipeline(query, df)
    return jsonify(response)

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def rag_pipeline(query, dataframe):
    relevant_data = dataframe[dataframe['name'].str.contains(query, case=False, na=False)]
    context = relevant_data.to_string(index=False)
    prompt = f"Answer the following question based on the context: {context}\n\nQuestion: {query}\nAnswer:"
    return generate_response(prompt)

if __name__ == '__main__':
    app.run(debug=True)
