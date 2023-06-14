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

model = tf.keras.models.load_model('./modelCapstone.h5')
data = pd.read_csv('ngirit_datasetnew.csv')
data = data.drop('merchant_area',axis=1).replace(to_replace = 'NAN', value=np.NaN)
data['rating'] = pd.to_numeric(data['rating'])
data['rating'].fillna(float(data['rating'].mean()),inplace=True)
data['combined_features'] = data[['merchant_name', 'main_category', 'sub_category', 'product']].apply(lambda x: ' '.join(x), axis=1)
cv = CountVectorizer()
label_encoder = LabelEncoder()
data['sub_category_encoded'] = label_encoder.fit_transform(data['sub_category'])
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
        money = float(req.text)
        print("Money:", money)
        sub_category = req.text
        print("Category:", sub_category)

        input_data = pd.DataFrame({'price': [money], 'sub_category': [sub_category]})
        input_data['rating'] = data['rating'].mean()
        input_data['sub_category_encoded'] = label_encoder.transform(input_data['sub_category'])
        print(input_data)
        input_data['combined_features'] = input_data[['sub_category']].apply(lambda x: ' '.join(x), axis=1)

        input_features = cv.transform(input_data['combined_features']).toarray()

        predictions = model.predict(input_features)
        predicted_class = np.argmax(predictions)

        filtered_data = data[(data['sub_category_encoded'] == predicted_class) & (data['price'] <= money)]

        if filtered_data.empty:
            print(f'Tidak ada rekomendasi yang sesuai dengan jumlah uang Rp. {price}')

        sorted_data = filtered_data.sort_values(by=['rating', 'price'], ascending=[False, False])

        recommended_products = pd.DataFrame()
        merchant_counts = {} 
        for _, row in sorted_data.iterrows():
            merchant_name = row['merchant_name']

            if merchant_name not in merchant_counts:
                merchant_counts[merchant_name] = 0

            if merchant_counts[merchant_name] < 1:
                recommended_products = pd.concat([recommended_products, row.to_frame().T])
                merchant_counts[merchant_name] += 1

        return recommended_products[['product', 'merchant_name', 'price', 'rating']]
    except Exception as e:
        traceback.print_exc()
        response.status_code = 500
        return "Internal Server Error"
    
port = os.environ.get("PORT", 8080)
print(f"Listening to http://0.0.0.0:{port}")
uvicorn.run(app, host='0.0.0.0',port=port)