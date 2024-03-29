from agents.trip_planning_agent import TripPlanningAgent
from config import get_rapidapi_key

#testing find flight
departure = 'BOS' 
destination = 'LAX'  
date = '20240404'  
rapidapi_key = get_rapidapi_key()

trip_planner = TripPlanningAgent(departure, destination, date, rapidapi_key)

response = trip_planner.find_flights()

if response:
    flight_details_list = trip_planner.extract_flight_details(response)
    if flight_details_list:
        for idx, flight_details in enumerate(flight_details_list):
            print(f"Flight {idx + 1}:")
            print('Airline Name:', flight_details.get('airline_name'))
            print('Origin Name:', flight_details.get('origin_name'))
            print('Destination Name:', flight_details.get('destination_name'))
            print('Flight Number:', flight_details.get('flight_number'))
            print('Trip Time:', flight_details.get('trip_time'))
            print()
    else:
        print("No flights found.")
else:
    print("No response received.")
