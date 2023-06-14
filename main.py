from flask import Flask, request, jsonify
from predict_and_recommend_products import predict_and_recommend_products
from preprocessed_data import data

app = Flask(__name__)

@app.route("/")
def home():
    return "C23-PR488"

@app.route("/recommend", methods=["POST"])
def recommend():
    if request.method == 'POST':
        money = float(request.form.get("money"))
        sub_category = request.form.get("sub_category")
    recommended_products = predict_and_recommend_products(money, sub_category, data)

    if recommended_products is None:
        return jsonify({"error": "No recommendations found"})
    else:
        results = []
        for i, row in recommended_products.iterrows():
            product = row['product']
            merchant_name = row['merchant_name']
            price = row['price']
            rating = row['rating']
            result = {
                "product": product,
                "merchant_name": merchant_name,
                "price": price,
                "rating": rating
            }
            results.append(result)

        return jsonify({"recommended_products": results})

if (__name__ == "__main__"):
     app.run(host="0.0.0.0", port = 5000, debug=False)
