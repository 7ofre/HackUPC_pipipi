from flask import Flask, request, render_template
import pandas as pd

def find_companions_by_date_location(traveler_name):
    data = pd.read_csv('dataset.csv')
    # Ensure date columns are in the correct datetime format
    data['Departure Date'] = pd.to_datetime(data['Departure Date'], format='%d/%m/%Y')
    data['Return Date'] = pd.to_datetime(data['Return Date'], format='%d/%m/%Y')
    
    # Get the travel details of the specified traveler
    traveler_details = data[data['Traveller Name'] == traveler_name]
    
    # Initialize an empty list to collect potential companions
    potential_companions = []
    
    # Check each trip by the traveler for potential companions
    for _, trip in traveler_details.iterrows():
        # Identify other travelers in the same city with overlapping travel dates
        overlapping_travels = data[
            (data['Arrival City'] == trip['Arrival City']) &
            (data['Departure Date'] <= trip['Return Date']) &
            (data['Return Date'] >= trip['Departure Date']) &
            (data['Traveller Name'] != traveler_name)
        ]
        
        # Append overlapping travels to the potential_companions list
        for _, companion_trip in overlapping_travels.iterrows():
            potential_companions.append({
                'Traveller Name': companion_trip['Traveller Name'],
                'Departure Date': companion_trip['Departure Date'].strftime('%Y-%m-%d'),
                'Return Date': companion_trip['Return Date'].strftime('%Y-%m-%d')
            })
    
    return potential_companions

app = Flask(__name__, static_folder='static')

@app.route('/find-companions', methods=['POST'])
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
