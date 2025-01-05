from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import util  # Make sure util.py is in the same directory or accessible in your project

app = Flask(__name__)
CORS(app)  # Enabling CORS for all routes

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        # Call your util function to get the location names
        locations = util.get_location_names()  
        return jsonify({'locations': locations})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': 'Failed to fetch locations'}), 500

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        # Parse incoming JSON data
        data = request.get_json()  # Getting data from the JSON body
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        total_sqft = data.get('total_sqft')
        location = data.get('location')
        bhk = data.get('bhk')
        bath = data.get('bath')

        # Ensure all necessary fields are provided
        if total_sqft is None or location is None or bhk is None or bath is None:
            return jsonify({'error': 'Missing input fields'}), 400

        # Ensure that numeric values are valid
        try:
            total_sqft = float(total_sqft)
            bhk = int(bhk)
            bath = int(bath)
        except ValueError:
            return jsonify({'error': 'Invalid number format for sqft, bhk, or bath'}), 400

        # Calling the util function to get the estimated price
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

        return jsonify({'estimated_price': estimated_price})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': "Invalid input or server error."}), 400

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    try:
        util.load_saved_artifacts()  # Make sure your model or artifacts are loaded properly
    except Exception as e:
        print(f"Error loading artifacts: {e}")
        exit(1)  # Exit if the artifacts cannot be loaded

    # Dynamic port binding for deployment platforms
    port = int(os.environ.get('PORT', 5000))  # Use PORT env variable if available, else default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
