import os
import uvicorn
import traceback
import tensorflow as tf
import pandas as pd
import numpy as np

from pydantic import BaseModel
from urllib.request import Request
from fastapi import FastAPI, Response, UploadFile
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

# Initialize Model
# If you already put yout model in the same folder as this main.py
# You can load .h5 model or any model below this line

# If you use h5 type uncomment line below
model = tf.keras.models.load_model('./modelCapstone.h5')
data = pd.read_csv('ngirit_datasetnew.csv')
data['combined_features'] = data[['merchant_name', 'main_category', 'sub_category', 'product']].apply(lambda x: ' '.join(x), axis=1)
cv = CountVectorizer()
cv.fit(data['combined_features'])

app = FastAPI()

# This endpoint is for a test (or health check) to this server
@app.get("/")
def index():
    return "Hello world from ML endpoint!"

# If your model need text input use this endpoint!
class RequestText(BaseModel):
    text: str

@app.post("/predict_text")
def predict_text(req: RequestText, response: Response):
    try:
        # In here you will get text sent by the user
        money = req.text
        print("Money:", money)
        sub_category = req.text
        print("Category:", sub_category)
        # Step 1: (Optional) Do your text preprocessing
        # Create a dataframe with the input data
        input_data = pd.DataFrame({'price': [money], 'sub_category': [sub_category]})
    
        # Preprocess the input data
        input_data['rating'] = data['rating'].mean()  # Set the rating as the average rating in the dataset
        input_data['sub_category_encoded'] = label_encoder.transform(input_data['sub_category'])
        input_data['combined_features'] = input_data[['sub_category']].apply(lambda x: ' '.join(x), axis=1)
    
        # Transform the input data using the CountVectorizer
        input_features = cv.transform(input_data['combined_features']).toarray()
        # Step 2: Prepare your data to your model
        
        # Step 3: Predict the data
        # result = model.predict(...)
        # Make predictions using the trained model
        predictions = model.predict(input_features)
        # Step 4: Change the result your determined API output
        # Get the predicted class label
        predicted_class = np.argmax(predictions)
    
        # Filter the data based on the predicted class label and price range
        filtered_data = data[(data['sub_category_encoded'] == predicted_class) & (data['price'] <= price)]
    
        # Check if any recommendations are found
        if filtered_data.empty:
            print(f'Tidak ada rekomendasi yang sesuai dengan jumlah uang Rp. {price}')
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
        # return "Endpoint not implemented"
    except Exception as e:
        traceback.print_exc()
        response.status_code = 500
        return "Internal Server Error"
    
# Starting the server
# Your can check the API documentation easily using /docs after the server is running
port = os.environ.get("PORT", 8080)
print(f"Listening to http://0.0.0.0:{port}")
uvicorn.run(app, host='0.0.0.0',port=port)
