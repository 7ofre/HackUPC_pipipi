from flask import Flask, request
import pandas as pd

def find_companions_by_date_location(traveler_name):
    data = pd.read_csv('dataset.csv')
    # Ensure date columns are in the correct datetime format
    data['Departure Date'] = pd.to_datetime(data['Departure Date'], format='%d/%m/%Y')
    data['Return Date'] = pd.to_datetime(data['Return Date'], format='%d/%m/%Y')
    
    # Get the travel details of the specified traveler
    traveler_details = data[data['Traveller Name'] == traveler_name]
    
    # Initialize an empty DataFrame to collect potential companions
    potential_companions = pd.DataFrame()
    
    # Check each trip by the traveler for potential companions
    for _, trip in traveler_details.iterrows():
        # Identify other travelers in the same city with overlapping travel dates
        overlapping_travels = data[
            (data['Arrival City'] == trip['Arrival City']) &
            (data['Departure Date'] <= trip['Return Date']) &
            (data['Return Date'] >= trip['Departure Date']) &
            (data['Traveller Name'] != traveler_name)
        ]
        
        # Append overlapping travels to the potential_companions DataFrame
        potential_companions = pd.concat([potential_companions, overlapping_travels], ignore_index=True)
    
    # Select relevant information and remove any duplicates
    companions_details = potential_companions[['Traveller Name', 'Departure Date', 'Return Date']].drop_duplicates()
    
    return companions_details
# Assuming you have the data loaded in a DataFrame named 'travel_data'
# Example usage:
# companions = find_companions_by_date_location("Anderson Hudson", travel_data)
# print(companions)

app = Flask(__name__)

@app.route('/find-companions', methods=['POST'])
def indexPost():
    traveller_name = request.form['travellerName']
    companions = find_companions_by_date_location(traveller_name)
    return companions.to_json()

@app.route('/', methods=['GET'])
def indexGet():
    return """
    <h1>Enter Your Input</h1>
    <form method="post" action="/find-companions">
        <input type="text" name="travellerName" placeholder="Enter your input" required>
        <button type="submit">Submit</button>
    </form>
        """

if __name__ == '__main__':
    app.run(debug=True)
