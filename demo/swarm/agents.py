import json
from swarm import Agent
from anyactions import ActionHub


def find_flight(departure_id="", arrival_id="", type=2, outbound_date="", localization="", hl="", currency="", return_date="", travel_class=1, adults=1, children=0, infants_in_seat=0, infants_on_lap=0, bags=0, max_price=1000, output="json"):
    """Search for flights using the SerpAPI Google Flights API."""
    # You can customize the input parameters here
    input_params = locals()
    
    # safe_call will handle the authentication automatically
    response = hub.safe_call(action_name="serpapi_google_flights_search", input_params=input_params)
    
    # You can customize the tool response here
    return response

hub = ActionHub(observer=True) # enable observer to log tool calls

travel_agent = Agent(
    name="Travel Agent",
    instructions="You are a helpful agent.",
    functions=hub.tools_func([find_flight, "wikipedia_search"]), # Directly add the function or tool name you want to retrieved from AnyActions
)

