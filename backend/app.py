import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__, static_folder='static')

# Load the dataset
data = pd.read_csv('dataset.csv')
# Convert date columns to datetime objects for easier comparison
data['Departure Date'] = pd.to_datetime(data['Departure Date'], format='%d/%m/%Y')
data['Return Date'] = pd.to_datetime(data['Return Date'], format='%d/%m/%Y')

# Define function to find companions by traveler name
def find_companions_by_date_location(traveler_name):
    # Filter data for the specified traveler name
    traveler_data = data[data['Traveller Name'] == traveler_name]
    
    # Initialize list to store companions
    companions = []
    
    # Iterate over each row of traveler's data
    for index, trip in traveler_data.iterrows():
        # Filter data for overlapping trips in the same city
        overlapping_trips = data[
            (data['Arrival City'] == trip['Arrival City']) &
            (data['Departure Date'] <= trip['Return Date']) &
            (data['Return Date'] >= trip['Departure Date']) &
            (data['Traveller Name'] != traveler_name)
        ]
        
        # Iterate over each overlapping trip and extract companion details
        for _, companion_trip in overlapping_trips.iterrows():
            companions.append({
                'Name': companion_trip['Traveller Name'],
                'Departure Date': companion_trip['Departure Date'].strftime('%d/%m/%Y'),
                'Return Date': companion_trip['Return Date'].strftime('%d/%m/%Y'),
                'Shared Activities': list(set(trip['Activities'].split(', ')) & set(companion_trip['Activities'].split(', '))),
                'Arrival City': companion_trip['Arrival City']  # Include arrival city in companion details
            })
    
    return companions

# Define route for displaying companion results
@app.route('/find-companions', methods=['POST'])
def indexPost():
    traveler_name = request.form['travellerName']
    companions = find_companions_by_date_location(traveler_name)
    return render_template('results.html', companions=companions)

# Define route for the input form
@app.route('/', methods=['GET'])
def indexGet():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
