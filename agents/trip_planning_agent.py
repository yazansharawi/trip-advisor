import requests
import xml.etree.ElementTree as ET

class TripPlanningAgent:
    def __init__(self, departure, destination, date, rapidapi_key):
        self.departure = departure
        self.destination = destination
        self.date = date
        self.rapidapi_key = rapidapi_key

    def find_flights(self):
        url = f"https://timetable-lookup.p.rapidapi.com/TimeTable/{self.departure}/{self.destination}/{self.date}/"
        querystring = {"Max_Results": "10"}

        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "timetable-lookup.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        return response.text

    def extract_flight_details(self, xml_response):
        flight_details_list = []
        root = ET.fromstring(xml_response)
        ns = {'ota': 'http://www.opentravel.org/OTA/2003/05'}

        # Iterate through each FlightDetails node
        for flight_node in root.findall(".//ota:FlightDetails", namespaces=ns):
            flight_details = {}

            # Extract airline name
            airline_node = flight_node.find("./ota:MarketingAirline", namespaces=ns)
            if airline_node is not None:
                flight_details['airline_name'] = airline_node.get('CompanyShortName')

            # Extract origin and destination names
            origin_node = flight_node.find("./ota:DepartureAirport", namespaces=ns)
            destination_node = flight_node.find("./ota:ArrivalAirport", namespaces=ns)
            if origin_node is not None and destination_node is not None:
                flight_details['origin_name'] = origin_node.get('FLSLocationName')
                flight_details['destination_name'] = destination_node.get('FLSLocationName')

            # Extract trip time
            trip_time = flight_node.get('TotalTripTime')
            if trip_time:
                flight_details['trip_time'] = trip_time

            # Extract flight number
            flight_number = flight_node.get('FlightNumber')
            if flight_number:
                flight_details['flight_number'] = flight_number

            flight_details_list.append(flight_details)

        return flight_details_list