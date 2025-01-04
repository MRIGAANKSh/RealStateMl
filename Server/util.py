import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    try:
        # Check if the location exists in the data columns
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1  # Location not found in the list
    
    # Prepare the input feature vector for prediction
    x = np.zeros(len(__data_columns))
    x[0] = sqft  # square feet
    x[1] = bath   # number of bathrooms
    x[2] = bhk    # number of bedrooms
    if loc_index >= 0:
        x[loc_index] = 1  # Set the corresponding location feature
    
    # If location is invalid, raise an error
    if loc_index == -1:
        raise ValueError(f"Location '{location}' not found in the dataset.")
    
    # Predict and return the estimated price
    try:
        estimated_price = round(__model.predict([x])[0], 2)
        return estimated_price
    except Exception as e:
        print(f"Error in prediction: {e}")
        raise Exception("Error in prediction, check the model and input data.")

def load_saved_artifacts():
    print("Loading saved artifacts... start")
    global __data_columns
    global __locations

    try:
        # Load the columns (features) for the model
        with open("./columns.json", "r") as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]  # First 3 columns are sqft, bath, bhk
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure the 'columns.json' file exists in the correct directory.")
        raise e
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from columns.json: {e}")
        raise e

    try:
        # Load the trained model
        global __model
        if __model is None:
            with open("./realprice.pickle", "rb") as f:
                __model = pickle.load(f)
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure the 'realprice.pickle' file exists in the correct directory.")
        raise e
    except pickle.UnpicklingError as e:
        print(f"Error loading the model: {e}")
        raise e

    print("Loading saved artifacts... done")

def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    try:
        load_saved_artifacts()
        print(get_location_names())
        print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
        print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
        print(get_estimated_price('Kalhalli', 1000, 2, 2))  # Other location
        print(get_estimated_price('Ejipura', 1000, 2, 2))  # Other location
    except Exception as e:
        print(f"Error during price prediction: {e}")
