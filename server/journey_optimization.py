import networkx as nx
import numpy as np
import held_karp

import requests
import json

class Journey():
    def __init__(self,user,keep_points_interest,ratio_visit_travel=0.6):
        self.ratio_visit_travel = ratio_visit_travel #the heuristic ratio between time travelling and time visiting
        self.user = user
        self.keep_points_interest = keep_points_interest #the points of interest which have been kept
        self.journey =  self.initialize_journey() #the journey and 
        self.distance_matrix = self.get_distance_matrix() #the matrix containing the distances between each point
        # print(self.distance_matrix)
        self.journey_time = self.get_journey_time() #the duration of the journey

        
    def get_distance_matrix(self):
        """n = len(self.keep_points_interest)
        distance_matrix = np.zeros((n,n))"""
        locations = [elem.coord for elem in self.keep_points_interest]
        locations = [self.user.depar_loc] + locations + [self.user.arr_loc]
        # print(locations)
        MAPBOX_ACCESS_KEY = 'pk.eyJ1IjoibGFmaXVzIiwiYSI6ImNqdHZpZnl2YTFybTAzeWxsbjJvNjY5eW4ifQ.wirxUDiWbhISy5PGNBHp1A'
        ROUTE_URL = "https://api.mapbox.com/directions-matrix/v1/mapbox/walking/{0}?access_token={1}"
        lat_longs = ";".join(["{0},{1}".format(elem[0], elem[1]) for elem in locations])
        
        url = ROUTE_URL.format(lat_longs, MAPBOX_ACCESS_KEY)
        
        result = requests.get(url)
        result = result.json()
        return np.array(result['durations'])
        
    def get_travel_distance(self):
        index = [elem for elem in range(len(self.journey)+1)]
        index += [len(self.distance_matrix)-1]
        dist_mat = self.distance_matrix[index,:][:,index]
        opt, path = held_karp.held_karp(dist_mat)
        path[-1] = len(self.journey)+1
        self.optimal_path = path #returns the optimal path, useful for the visualization on the map
        return opt
    
    def initialize_journey(self):
        """Choose an initialization of the journey, here there is none
        """
        time_visiting = 0
        journey = []
        ind = 0
        """while time_visiting < self.ratio_visit_travel * self.user.time_available:
            journey += [self.keep_points_interest[ind]]
            ind += 1"""
        return journey
    
    def get_journey_time(self):
        self.travel_distance = self.get_travel_distance()
        #travel_time = self.travel_distance/self.user.travel_speed #travel_distance in km, user.travel_speed in km/h
        visiting_time = 0 
        for point_of_interest in self.journey:
            visiting_time += point_of_interest.visiting_time
        #return travel_time + visiting_time
        return self.travel_distance + visiting_time
    
    """def optimize_journey(self):
        while(self.journey_time>self.user.time_available or ):
            if self.journey_time>self.user.time_available:
                del self.journey[-1]
                self.journey_time = self.get_journey_time()
            else:
                self.journey += [self.keep_points_interest[len(self.journey)]]
                self.journey_time = self.get_journey_time()"""
                
    def optimize_journey(self):
        while(self.journey_time<self.user.time_available and len(self.journey)<=len(self.keep_points_interest)-1):
            self.journey += [self.keep_points_interest[len(self.journey)]]
            self.journey_time = self.get_journey_time()
            
    def get_schedule(self):
        schedule = np.zeros((len(self.journey)+1,2))
        for i in range(len(self.journey)):
            schedule[i+1,0] =  schedule[i,1] + self.distance_matrix[self.optimal_path[i],self.optimal_path[i+1]]
            schedule[i+1,1] = schedule[i+1,0] + self.journey[self.optimal_path[i+1] - 1].visiting_time
        return schedule[1:,:]
    
    def get_optimal_journey(self):
        self.optimize_journey()
        self.schedule = self.get_schedule()
        return self.journey, self.journey_time, self.travel_distance, self.optimal_path, self.schedule