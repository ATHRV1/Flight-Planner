from flight import Flight
from collections import deque


class MinHeap:
    def __init__(self, arr=None):
        self.heap = [] if arr is None else arr.copy()
        for i in range(len(self.heap) // 2, -1, -1):
            self._shift_down(i)

    def _shift_up(self, i):
        parent = (i - 1) // 2
        while i > 0 and self.heap[i][0] < self.heap[parent][0]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent
            parent = (i - 1) // 2

    def _shift_down(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i
        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._shift_down(smallest)

    def insert(self, element):
        self.heap.append(element)
        self._shift_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None
        min_val = self.heap[0]
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        self.heap.pop()
        if self.heap:
            self._shift_down(0)
        return min_val

    def is_empty(self):
        return len(self.heap) == 0


class PriorityQueue:
    def __init__(self):
        self.queue = MinHeap()

    def enqueue(self, element):
        self.queue.insert(element)

    def dequeue(self):
        return self.queue.extract_min()

    def is_empty(self):
        return self.queue.is_empty()


class Planner:
    def __init__(self, flights):
        self.flights = flights
        self.adj_list = {}

        for flight in flights:
            self.adj_list[flight] = []

        flights_by_start = {}
        for flight in flights:
            if flight.start_city not in flights_by_start:
                flights_by_start[flight.start_city] = []
            flights_by_start[flight.start_city].append(flight)

        for flight1 in flights:
            if flight1.end_city in flights_by_start:
                for flight2 in flights_by_start[flight1.end_city]:
                    if flight2.departure_time >= flight1.arrival_time + 20:
                        self.adj_list[flight1].append(flight2)


    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        if not self.flights:
            return []
        
        if t1 > t2 or start_city == end_city:
            return []

        start_flights = []
        for flight in self.flights:
            if (
                flight.start_city == start_city
                and flight.departure_time >= t1
                and flight.arrival_time <= t2
            ):
                start_flights.append(flight)

        if not start_flights:
            return []

        start_flights.sort(key=lambda x: x.departure_time)

        queue = deque()
        visited = set()
        min_flights = float("inf")
        earliest_arrival = float("inf")
        best_route = None

        for flight in start_flights:
            queue.append((flight, [flight], 1)) 

        while queue:
            current_flight, path, num_flights = queue.popleft()

            if num_flights > min_flights:
                continue

            if current_flight.end_city == end_city:
                current_arrival = path[-1].arrival_time

                if num_flights < min_flights or (
                    num_flights == min_flights and current_arrival < earliest_arrival
                ):
                    min_flights = num_flights
                    earliest_arrival = current_arrival
                    best_route = path.copy()
                continue

            for next_flight in self.adj_list[current_flight]:
                if (
                    next_flight.arrival_time <= t2
                    and (next_flight, num_flights + 1) not in visited
                ):
                    visited.add((next_flight, num_flights + 1))
                    queue.append((next_flight, path + [next_flight], num_flights + 1))

        return best_route if best_route else []

    def cheapest_route(self, start_city, end_city, t1, t2):
        if not self.flights:
            return []
        
        if t1 > t2 or start_city == end_city:
            return []
    
        start_flights = []
        for flight in self.flights:
            if (flight.start_city == start_city and 
                flight.departure_time >= t1 and 
                flight.arrival_time <= t2):
                start_flights.append(flight)
    
        if not start_flights:
            return []
    
        distances = {flight: float('inf') for flight in self.flights}
        previous = {flight: None for flight in self.flights}
        visited=set()
        
        pq = PriorityQueue()
        for flight in start_flights:
            distances[flight] = flight.fare
            pq.enqueue((flight.fare, flight))
    
        while not pq.is_empty():
            current_cost, current_flight = pq.dequeue()

            if current_flight in visited:
                continue
            
            visited.add(current_flight)
            
            if current_flight.end_city == end_city:
                break
                
            if current_cost > distances[current_flight]:
                continue
                
            for next_flight in self.adj_list[current_flight]:
                if next_flight.arrival_time <= t2:
                    new_cost = current_cost + next_flight.fare
                    
                    if new_cost < distances[next_flight]:
                        distances[next_flight] = new_cost
                        previous[next_flight] = current_flight
                        pq.enqueue((new_cost, next_flight))
    
        route = []
        min_cost = float('inf')
        last_flight = None
    
        for flight in self.flights:
            if (flight.end_city == end_city and 
                distances[flight] < min_cost and 
                flight.arrival_time <= t2):
                min_cost = distances[flight]
                last_flight = flight
    
        if last_flight is None:
            return []
    
        current_flight = last_flight
        while current_flight is not None:
            route.append(current_flight)
            current_flight = previous[current_flight]
    
        route.reverse()
        return route

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        if not self.flights:
            return []
        if t1 > t2 or start_city == end_city:
            return []   
        start_flights = []
        for flight in self.flights:
            if (flight.start_city == start_city and 
                flight.departure_time >= t1 and 
                flight.arrival_time <= t2):
                start_flights.append(flight)
        
        if not start_flights:
            return []
            
        distances = {flight: (float('inf'), float('inf')) for flight in self.flights} 
        previous = {flight: None for flight in self.flights}
        
        pq = PriorityQueue()
        
        for flight in start_flights:
            distances[flight] = (1, flight.fare)  
            pq.enqueue(((1, flight.fare), flight)) 
        
        while not pq.is_empty():
            (num_flights, cost), current_flight = pq.dequeue()
            
            if (num_flights, cost) > distances[current_flight]:
                continue
                
            for next_flight in self.adj_list[current_flight]:
                if next_flight.arrival_time <= t2:
                    new_num_flights = num_flights + 1
                    new_cost = cost + next_flight.fare
                    
                    if ((new_num_flights, new_cost) < distances[next_flight]):
                        distances[next_flight] = (new_num_flights, new_cost)
                        previous[next_flight] = current_flight
                        pq.enqueue(((new_num_flights, new_cost), next_flight))
        
        best_flight = None
        best_metric = (float('inf'), float('inf'))
        
        for flight in self.flights:
            if (flight.end_city == end_city and 
                distances[flight] < best_metric):
                best_metric = distances[flight]
                best_flight = flight
                
        if best_flight is None:
            return []
            
        route = []
        current_flight = best_flight
        while current_flight is not None:
            route.append(current_flight)
            current_flight = previous[current_flight]
            
        route.reverse()
        return route


