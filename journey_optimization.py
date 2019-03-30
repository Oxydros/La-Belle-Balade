#%%
import os
os.chdir('C:/ML-Tools/ACE-1.2.15/FacebookHack2019')

import networkx as nx
import numpy as np
import held_karp

import requests
import json



class Journey():
    def __init__(self,user,ratio_visit_travel=0.6):
        self.ratio_visit_travel = ratio_visit_travel #the heuristic ratio between time travelling and time visiting
        self.user = user
        self.journey =  self.initialize_journey() #the journey and 
        self.distance_matrix = self.get_distance_matrix #the matrix containing the distances between each point
        self.journey_time = self.get_journey_time() #the duration of the journey

        
    def get_distance_matrix(self):
        """n = len(self.user.keep_point_interest)
        distance_matrix = np.zeros((n,n))"""
        locations = [elem.coord for elem in self.user.keep_point_of_interest]
        MAPBOX_ACCESS_KEY = 'pk.eyJ1IjoibGFmaXVzIiwiYSI6ImNqdHZpZnl2YTFybTAzeWxsbjJvNjY5eW4ifQ.wirxUDiWbhISy5PGNBHp1A'
        ROUTE_URL = "https://api.mapbox.com/directions-matrix/v1/mapbox/walking/{0}?access_token={1}"
        lat_longs = ";".join(["{0},{1}".format(elem[0], elem[1]) for elem in locations])
        
        url = ROUTE_URL.format(lat_longs, MAPBOX_ACCESS_KEY)
        
        result = requests.get(url)
        result = result.json()
        return result['durations']
        
    def get_travel_distance(self):
        opt, path = held_karp(self.distance_matrix)
        self.optimal_path = path #returns the optimal path, useful for the visualization on the map
        return opt
    
    def initialize_journey(self):
        """Choose an initialization of the journey, here there is none
        """
        time_visiting = 0
        journey = []
        ind = 0
        """while time_visiting < self.ratio_visit_travel * self.user.time_available:
            journey += [self.user.keep_point_interest[ind]]
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
                self.journey += [self.user.keep_point_interest[len(self.journey)]]
                self.journey_time = self.get_journey_time()"""
                
    def optimize_journey(self):
        while(self.journey_time<self.user.time_available):
            self.journey += [self.user.keep_point_interest[len(self.journey)]]
            self.journey_time = self.get_journey_time()
    
    def get_optimal_journey(self):
        self.optimize_journey()
        return self.journey, self.journey_time, self.travel_distance, self.optimal_path