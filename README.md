# Ngirit-Machine

## Dataset & Preprocessing
1. We obtained the raw dataset from [here](https://www.kaggle.com/datasets/ariqsyahalam/indonesia-food-delivery-gofood-product-list).
2. The dataset contains the names of merchants and their products in three cities: Surabaya, Medan, and Jakarta (Jabodetabek). We decided to only use merchants from Jakarta (Jabodetabek) and eliminate the rest.
3. We manually added the location (latitude, longitude) from Google Maps based on the merchant names in the dataset.
5. We added a new feature called 'rating' to the dataset to increase the variety of food recommendations.
6. The 'rating' feature was obtained from the Gofood platform, and we manually eliminated merchants that had permanently closed.
7. We added the 'main_category' feature to map each menu item as either 'food' or 'beverage'.
8. We changed the 'Category of product' feature to 'sub_category' and mapped each data point to only one category. For example, 'Kopi/Minuman/Roti' became 'Kopi' based on the product name. We did this manually.
9. We removed the 'merchant_area', 'display', 'discount_price', 'isDiscount', and 'description' features.
10. ngirit_datasetnew.csv is the dataset that we have preprocessed manually.

## Advanced Preprocessing
1. We changed the data type of the 'rating' feature to numeric.
2. We handled missing values in the 'rating' feature using mean imputation.
3. We performed encoding on the target variable (ordinal encoding).
4. We performed a join on the 'merchant_name', 'main_category', 'sub_category', and 'product' features.
4. We transformed the resulting joined features into a keyword matching matrix.

## The Model
