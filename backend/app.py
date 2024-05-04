from flask import Flask, request, render_template
import pandas as pd

from datetime import datetime
import pandas as pd
data = pd.read_csv('dataset.csv')
# Convert date columns to datetime objects for easier comparison
data['Departure Date'] = pd.to_datetime(data['Departure Date'], format='%d/%m/%Y')
data['Return Date'] = pd.to_datetime(data['Return Date'], format='%d/%m/%Y')

def find_companions_by_date_location(name):
    # Filter for the trips of the given traveller
    person_trips = data[data['Traveller Name'] == name]
    if person_trips.empty:
        return f"No trips found for {name}."
    
    companions = []

    # Loop through each trip of the person
    for index, trip in person_trips.iterrows():
        # Find other people in the same city during the overlapping period
        overlapping_trips = data[(data['Arrival City'] == trip['Arrival City']) &
                                 (data['Departure Date'] <= trip['Return Date']) &
                                 (data['Return Date'] >= trip['Departure Date']) &
                                 (data['Traveller Name'] != name)]
        
        # Loop through each overlapping trip and collect details
        for _, companion_trip in overlapping_trips.iterrows():
            companions.append({
                'Name': companion_trip['Traveller Name'],
                'Departure Date': companion_trip['Departure Date'].strftime('%d/%m/%Y'),
                'Return Date': companion_trip['Return Date'].strftime('%d/%m/%Y'),
                'Shared Activities': list(set(trip['Activities'].split(', ')) & set(companion_trip['Activities'].split(', ')))
            })

    return companions if companions else f"No companions found for {name} during their trips."

# Assuming you have the data loaded in a DataFrame named 'travel_data'
# Example usage:
# companions = find_companions_by_date_location("Anderson Hudson", travel_data)
# print(companions)



app = Flask(__name__, static_folder='static')

@app.route('/find-companions', methods=['POST'])
def indexPost():
    traveller_name = request.form['travellerName']
    companions = find_companions_by_date_location(traveller_name)
    return render_template('results.html', companions=companions)

@app.route('/', methods=['GET'])
def indexGet():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)