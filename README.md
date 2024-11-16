Flight Planner
Overview
This Flight Planner project aims to provide efficient solutions for travelers with different priorities when booking flights. The system optimizes routes based on three main criteria:

Route 1 - Fewest Flights and Earliest: The route with the least number of flights, and if multiple routes have the same number of flights, the one with the earliest arrival time.
Route 2 - Cheapest Trip: The route with the lowest total fare, regardless of the number of flights.
Route 3 - Fewest Flights and Cheapest: The route with the least number of flights, and if multiple options meet this, the one with the lowest fare.
Additionally, the planner ensures that there is a 20-minute gap between the arrival of one flight and the departure of the next connecting flight.

Requirements
The system consists of the following:

Flight Class (flight.py):

Represents a flight with the attributes: flight number, start city, departure time, end city, arrival time, and fare.
Planner Class (planner.py):

The core of the flight planning system, which uses a list of Flight objects to find optimized routes based on different goals.
Contains the following methods:
__init__(self, flights): Initializes the planner with a list of Flight objects.
least_flights_ealiest_route(self, start_city, end_city, t1, t2): Finds the route with the fewest flights and earliest arrival.
cheapest_route(self, start_city, end_city, t1, t2): Finds the route with the lowest total fare.
least_flights_cheapest_route(self, start_city, end_city, t1, t2): Finds the route with the fewest flights and cheapest fare.
Additional Considerations:

The planner ensures that each consecutive flight has a 20-minute gap between the arrival and departure times.
The time complexity of methods should adhere to the following:
__init__: O(m)
least_flights_ealiest_route: O(m)
cheapest_route: O(m log m)
least_flights_cheapest_route: O(m log m)


Final Notes
Ensure that all flight times respect the 20-minute gap rule for connecting flights.
If any route does not exist that satisfies the criteria, the method will return an empty list.
The solution is optimized to meet the worst-case time complexity requirements, ensuring efficient handling of up to 1000 test cases.
