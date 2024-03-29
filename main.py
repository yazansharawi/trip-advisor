from agents.trip_planning_agent import TripPlanningAgent
from config import get_rapidapi_key

departure = 'BOS' 
destination = 'Amman' 
date = '2024-04-04'
dateoff = '2024-04-05'   
rapidapi_key = get_rapidapi_key()

trip_planner = TripPlanningAgent(departure, destination, date, rapidapi_key)

