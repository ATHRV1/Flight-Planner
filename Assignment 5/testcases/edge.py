import random
import time
from tqdm import tqdm  # For progress bar
import os
from flight import Flight
from planner import Planner

def parse_test_case(file_path):
    try:
        print(f"Attempting to read file: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
            
        with open(file_path, 'r') as file:
            n, m = map(int, file.readline().strip().split())  # Read number of vertices and edges
            print(f"Reading {m} flights between {n} cities")
            
            flights = []
            cities = set()  # To keep track of all unique cities
            
            for i in range(m):
                line = file.readline().strip()
                try:
                    u, v, cost, start_time, end_time = map(int, line.split())
                    flight = Flight(len(flights), u, start_time, v, end_time, cost)
                    flights.append(flight)
                    cities.update([u, v])
                except ValueError as e:
                    print(f"Error parsing flight {i+1}: {line}")
                    raise
            
            print(f"Successfully parsed {len(flights)} flights and found {len(cities)} cities")
            return flights, list(cities)
            
    except Exception as e:
        print(f"Error in parse_test_case: {str(e)}")
        raise

def write_to_output(output_file, message):
    try:
        output_file.write(message + "\n")
        output_file.flush()  # Force write to disk
    except Exception as e:
        print(f"Error writing to output file: {str(e)}")
        raise

def main():
    try:
        # Use current directory if full path doesn't work
        current_dir = os.path.dirname(os.path.abspath(__file__))
        default_file_path = os.path.join(current_dir, 'C.txt')
        default_output_path = os.path.join(current_dir, 'received_output.txt')
        
        # Try the original paths first, then fall back to current directory
        file_path = r'C:\Users\HP\Flight Planner\Assignment 5\C.txt'
        output_path = r'C:\Users\HP\Flight Planner\Assignment 5\recieved_output.txt'
        
        if not os.path.exists(file_path):
            print(f"Warning: Could not find file at {file_path}")
            print(f"Trying alternate path: {default_file_path}")
            file_path = default_file_path
            output_path = default_output_path
        
        print(f"Using input file: {file_path}")
        print(f"Using output file: {output_path}")
        
        flights, cities = parse_test_case(file_path)
        print(f"Creating flight planner with {len(flights)} flights")
        flight_planner = Planner(flights)
        
        # Set random seed for consistent results
        random.seed(13)
        
        # Generate all unique pairs of cities
        city_pairs = [(start, dest) for start in cities for dest in cities if start != dest]
        print(f"Generated {len(city_pairs)} possible city pairs")
        
        # Randomly select 20 unique pairs
        num_pairs = min(20, len(city_pairs))  # In case we have fewer than 20 possible pairs
        sampled_pairs = random.sample(city_pairs, num_pairs)
        print(f"Selected {len(sampled_pairs)} pairs for testing")
        
        with open(output_path, 'w') as output_file:
            print("Opened output file successfully")
            overall_start_time = time.time()
            
            for start_city, destination in tqdm(sampled_pairs, desc="Processing city pairs", unit="pair"):
                try:
                    start_time = time.time()
                    write_to_output(output_file, f"\nTesting routes for start_city={start_city}, destination={destination}")
                    
                    # Task 1
                    print(f"Running Task 1 for {start_city} to {destination}")
                    route1 = flight_planner.least_flights_earliest_route(start_city, destination, 0, 3000000000000)
                    if route1:
                        num_flights_task1 = len(route1)
                        arrival_time_task1 = route1[-1].arrival_time if num_flights_task1 > 0 else None
                        write_to_output(output_file, f"Task 1: Least Flights Earliest Route - Number of flights: {num_flights_task1}, Arrival time: {arrival_time_task1}")
                    else:
                        write_to_output(output_file, "Task 1: No route found.")
                    
                    # Task 2
                    print(f"Running Task 2 for {start_city} to {destination}")
                    route2 = flight_planner.cheapest_route(start_city, destination, 0, 3000000000000)
                    if route2:
                        total_cost_task2 = sum(flight.fare for flight in route2)
                        write_to_output(output_file, f"Task 2: Cheapest Route - Total cost: {total_cost_task2}")
                    else:
                        write_to_output(output_file, "Task 2: No route found.")
                    
                    # Task 3
                    print(f"Running Task 3 for {start_city} to {destination}")
                    route3 = flight_planner.least_flights_cheapest_route(start_city, destination, 0, 30000000000)
                    if route3:
                        num_flights_task3 = len(route3)
                        total_cost_task3 = sum(flight.fare for flight in route3)
                        write_to_output(output_file, f"Task 3: Least Flights Cheapest Route - Number of flights: {num_flights_task3}, Total cost: {total_cost_task3}")
                    else:
                        write_to_output(output_file, "Task 3: No route found.")
                    
                    time_taken = time.time() - start_time
                    write_to_output(output_file, f"Time taken for start_city={start_city}, destination={destination}: {time_taken:.2f} seconds\n")
                
                except Exception as e:
                    print(f"Error processing pair {start_city}->{destination}: {str(e)}")
                    write_to_output(output_file, f"Error processing pair {start_city}->{destination}: {str(e)}\n")
            
            overall_time_taken = time.time() - overall_start_time
            write_to_output(output_file, f"Total time taken for all tests: {overall_time_taken:.2f} seconds")
            print("Testing completed successfully")
            
    except Exception as e:
        print(f"Critical error in main: {str(e)}")
        raise

if __name__ == "__main__":  # Fixed the main check
    main()