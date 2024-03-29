import requests
import xml.etree.ElementTree as ET

querystring = {"Max_Results": "10"}

class TripPlanningAgent:
    
    def __init__(self, departure, destination, date, rapidapi_key):
        self.departure = departure
        self.destination = destination
        self.date = date
        self.rapidapi_key = rapidapi_key

    def find_flights(self):
        url = f"https://timetable-lookup.p.rapidapi.com/TimeTable/{self.departure}/{self.destination}/{self.date}/"

        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "timetable-lookup.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        return response.text
    

    def find_hotels(self, region_id, checkin_date, checkout_date, rapidapi_key):
        url = "https://hotels-com-provider.p.rapidapi.com/v2/hotels/search"
        querystring = {
            "region_id": region_id,
            "locale": "en_GB",
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "adults_number": "1",  
            "page_number": "1" ,
            "domain":'AE',
            "sort_order": 'REVIEW',
        }

        headers = {
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            return response.json()  
        else:
            return None 

    

    def get_region_id(self, destination, rapidapi_key):
        url = "https://hotels-com-provider.p.rapidapi.com/v2/regions"
        querystring = {"query": destination, "domain": "AE", "locale": "en_GB"}
        headers = {
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
            }
        response = requests.get(url, headers=headers, params=querystring)
        regions = response.json() 
        
        if regions.get('data'):
            for region_data in regions['data']:
                if region_data.get('@type') == 'gaiaRegionResult' and region_data.get('type') == 'MULTICITY':  
                    return region_data['gaiaId'] 
                return None 
            else:
                return None 

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