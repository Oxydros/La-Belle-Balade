#%%
import networkx as nx
import numpy as np
import held_karp

class Journey():
    def __init__(self,user,ratio_visit_travel=0.6):
        self.ratio_visit_travel = ratio_visit_travel #the heuristic ratio between time travelling and time visiting
        self.user = user
        self.journey =  self.initialize_journey() #the journey and 
        self.distance_matrix = self.get_distance_matrix #the matrix containing the distances between each point
        self.journey_time = self.get_journey_time() #the duration of the journey
        
        
    def get_distance_matrix(self,):
        
    def get_travel_distance(self):
        opt, path = 
    
    
    def initialize_journey(self):
        time_visiting = 0
        journey = []
        ind = 0
        while time_visiting < self.ratio_visit_travel * self.user.time_available:
            journey += [self.user.keep_point_interest[ind]]
            ind += 1
        return journey
    
    def get_journey_time(self):
        self.travel_distance = self.get_travel_distance()
        travel_time = self.travel_distance/self.user.travel_speed #travel_distance in km, user.travel_speed in km/h
        visiting_time = 0 
        for point_of_interest in self.journey:
            visiting_time += point_of_interest.visiting_time
        return travel_time + visiting_time
    
    def optimize_journey(self):
        while(self.journey_time>self.user.time_available or ):
            if self.journey_time>self.user.time_available:
                del self.journey[-1]
                self.journey_time = self.get_journey_time()
            else:
                self.journey += [self.user.keep_point_interest[len(self.journey)]]
                self.journey_time = self.get_journey_time()