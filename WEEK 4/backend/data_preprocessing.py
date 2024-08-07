import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_restaurant_data(input_file, output_file):
    # Load the data
    restaurants_df = pd.read_csv(input_file)

    # Fill missing values for 'price_level' with the mean value
    restaurants_df['price_level'].fillna(restaurants_df['price_level'].mean(), inplace=True)

    # Fill missing values for 'opening_hours' with a placeholder
    restaurants_df['opening_hours'].fillna('Unknown', inplace=True)

    # Convert 'price_level' to integer (after filling NaNs)
    restaurants_df['price_level'] = restaurants_df['price_level'].astype(int)

    # Standardization
    scaler = StandardScaler()
    restaurants_df[['price_level', 'rating', 'user_ratings_total']] = scaler.fit_transform(
        restaurants_df[['price_level', 'rating', 'user_ratings_total']])

    # Save the processed data to a CSV file
    restaurants_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    preprocess_restaurant_data('data/restaurants_IP.csv', 'data/cleaned_restaurants.csv')
