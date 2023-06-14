import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
from preprocessed_data import data

def predict_and_recommend_products(price, sub_category, data):
    if sub_category not in data['sub_category'].values:
        return None

    # Create a dataframe with the input data
    input_data = pd.DataFrame({'price': [price], 'sub_category': [sub_category]})
    
    # Preprocess the input data
    input_data['rating'] = data['rating'].mean()  # Set the rating as the average rating in the dataset
    input_data['sub_category_encoded'] = LabelEncoder.transform(input_data['sub_category'])
    input_data['combined_features'] = input_data[['sub_category']].apply(lambda x: ' '.join(x), axis=1)
    
    # Transform the input data using the CountVectorizer
    input_features = CountVectorizer.transform(input_data['combined_features']).toarray()

    # Load model
    model = load_model('modelCaptsone', compile=False)

    # Make predictions using the trained model
    predictions = model.predict(input_features)

    # Get the predicted class label
    predicted_class = np.argmax(predictions)
    
    # Filter the data based on the predicted class label and price range
    filtered_data = data[(data['sub_category_encoded'] == predicted_class) & (data['price'] <= price)]
    
    # Check if any recommendations are found
    if filtered_data.empty:
        return None

    # Sort the filtered data based on rating in descending order, then by price in ascending order
    sorted_data = filtered_data.sort_values(by=['rating', 'price'], ascending=[False, False])
    
    # Select the top 10 recommended products
    recommended_products = pd.DataFrame()
    merchant_counts = {}  # Dictionary to store the count of recommendations for each merchant
    
    for _, row in sorted_data.iterrows():
        merchant_name = row['merchant_name']
        
        if merchant_name not in merchant_counts:
            merchant_counts[merchant_name] = 0
        
        if merchant_counts[merchant_name] < 1:
            recommended_products = pd.concat([recommended_products, row.to_frame().T])
            merchant_counts[merchant_name] += 1

    return recommended_products[['product', 'merchant_name', 'price', 'rating']]
