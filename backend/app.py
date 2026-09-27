# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from model_utils import clean_categories
from flask import Flask, request, Response jsonify  # For creating the Flask API

#Initialize the Flask application
superkart_predictor_api = Flask("Super Kart Sales Forecast Predictor")

# Load the trained machine learning model
model = joblib.load("superKart_Sales_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@superkart_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Super Kart Sales Prediction API!"

# Define an endpoint for single property prediction (POST request)
@superkart_predictor_api.post('/v1/sales')
def predict_sales():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        "Product_Weight": property_data["Product_Weight"],
        "Product_Sugar_Content": property_data["Product_Sugar_Content"],
        "Product_Allocated_Area": property_data["Product_Allocated_Area"],
        "Product_MRP": property_data["Product_MRP"],
        "Store_Size": property_data["Store_Size"],
        "Store_Location_City_Type": property_data["Store_Location_City_Type"],
        "Store_Type": property_data["Store_Type"],
        "Product_Id_char": property_data["Product_Id_char"],
        "Store_Age_Years": property_data["Store_Age_Years"],
        "Product_Type_Category": property_data["Product_Type_Category"]
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    predicted_sales = model.predict(input_data)[0]

    # Convert predicted_price to Python float
    predicted_sales = round(float(predicted_sales), 2)

    # Return the actual price
    return jsonify({'Predicted Sales (in dollars)': predicted_sales})


# Define an endpoint for batch prediction (POST request)
@superkart_predictor_api.post('/v1/salesbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Create output dataframe so the original input is not modified
    output_data = input_data.copy()

    # Make predictions for all properties in the DataFrame 
    predicted_sales = model.predict(input_data).tolist()

    # Add predictions as a new column
    output_data["Predicted_Sales"] = predicted_sales    


    # Convert DataFrame to CSV
    csv_output = output_data.to_csv(index=False)

    # Return CSV file in HTTP response
    return Response(
        csv_output,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=superkart_sales_predictions.csv"
        }
    )

if __name__ == '__main__':
    superkart_predictor_api.run(debug=True)
