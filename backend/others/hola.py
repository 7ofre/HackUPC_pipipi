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