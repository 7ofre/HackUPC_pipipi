from flask import Flask, request
import pandas as pd

def find_companions_by_date_location(traveler_name, data):
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

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_data = request.form['inputData']
        output_data = find_companions_by_date_location(input_data, dataset.csv)
        return output_data
    else:
        return """
        <h1>Enter Your Input</h1>
        <form method="post">
            <input type="text" name="inputData" placeholder="Enter your input" required>
            <button type="submit">Submit</button>
        </form>
        """

if __name__ == '__main__':
    app.run(debug=True)
