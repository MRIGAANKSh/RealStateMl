// Get the selected value of the bathroom radio buttons
function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    for (var i = 0; i < uiBathrooms.length; i++) {
        if (uiBathrooms[i].checked) {
            return parseInt(uiBathrooms[i].value);  // Return the value of the checked radio
        }
    }
    return -1;  // Invalid Value
}

// Get the selected value of the BHK radio buttons
function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    for (var i = 0; i < uiBHK.length; i++) {
        if (uiBHK[i].checked) {
            return parseInt(uiBHK[i].value);  // Return the value of the checked radio
        }
    }
    return -1;  // Invalid Value
}

// Triggered when the "Estimate Price" button is clicked
function onClickedEstimatePrice(event) {
    event.preventDefault();  // Prevent form submission

    console.log("Estimate price button clicked");

    // Get the values entered/selected by the user
    var sqft = document.getElementById("uiSqft");
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    var location = document.getElementById("uiLocations");
    var estPrice = document.getElementById("uiEstimatedPrice");

    // Prepare the data to send to the backend
    var requestData = {
        total_sqft: parseFloat(sqft.value),
        bhk: bhk,
        bath: bathrooms,
        location: location.value
    };

    // Backend URL for prediction request
    var url = "https://realstateml.onrender.com/predict_home_price";

    // Make POST request to the backend with JSON data
    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(requestData),  // Send data as JSON string
        success: function(data, status) {
            console.log(data.estimated_price);
            estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
            console.log(status);
        },
        error: function(xhr, status, error) {
            estPrice.innerHTML = "<h2>Failed to fetch prediction. Ensure the backend is running.</h2>";
            console.error("Error: ", error);
        }
    });
}

// Called when the page loads
function onPageLoad() {
    console.log("Document loaded");

    // Backend URL to fetch locations
    var url = "https://realstateml.onrender.com/get_location_names";

    // Fetch locations from backend
    $.get(url, function(data, status) {
        console.log("Got response for get_location_names request");
        if (data.locations) {
            var locations = data.locations;
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            for (var i = 0; i < locations.length; i++) {
                var opt = new Option(locations[i]);
                uiLocations.add(opt);
            }
        }
    }).fail(function() {
        console.error("Failed to fetch locations. Ensure the backend is running.");
    });
}

// Ensure the locations are loaded when the page is loaded
window.addEventListener('load', onPageLoad);
