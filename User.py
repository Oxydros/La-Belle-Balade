#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:07:45 2019

@author: geoffreycideron
"""

import numpy as np 

class User:
    def __init__(self, profile, depar_loc, arr_loc, time_available, keep_point_interests=10, travel_speed=4) :
        self.profile = profile
        self.depar_loc = depar_loc #(lamb, phi) => longitude et latitude
        self.arr_loc = arr_loc
        # Calculate the mid point of the journey
        self.mid_point = self.get_mid_point(self.depar_loc, self.arr_loc)
        self.dist_mid_depar = self.distance(self.mid_point,self.depar_loc)
        self.time_available = time_available
        self.keep_point_interests = keep_point_interests
        self.travel_speed = travel_speed
    
    def distance(self, point_a, point_b):
        x = (point_a[0]-point_b[0])*np.cos((point_a[1]+point_b[1])/2)
        y = (point_a[1]-point_b[1])
        return np.sqrt(x**2 + y**2)*6.371
    
    def get_mid_point(self, depar_loc, arr_loc):
        """
        Create the mid point of the journey
        """
        
        delta_lambda = depar_loc[0] - arr_loc[0]
        B_x = np.cos(depar_loc[1]*np.cos(delta_lambda))
        B_y = np.sin(depar_loc[1]*np.cos(delta_lambda))
        
        mid_phi = np.arctan2(np.sin(arr_loc[1]) + np.sin(depar_loc[1]), np.sqrt((np.cos(arr_loc[1]) + B_x)**2 + B_y**2))
        mid_lamb = arr_loc[0]  + np.arctan2(B_y, np.cos(arr_loc[1]) + B_x)
        
        return (mid_lamb, mid_phi)
    
    def distance_regularization(self, point_of_interest_dist):
        """
        Penalisation of the score if the point of interest is farther than the distance
        between the departure point and the mid point
        """
        if self.dist_mid_depar > point_of_interest_dist:
            return 1
        else:
            return np.exp(-(point_of_interest_dist - self.dist_mid_depar))
        
    def find_relevant_interest_points(self, points_of_interest):
        """
        Return the importance of each point of interest for the user
        """
        score = np.zeros(len(points_of_interest))
        for ind, point_of_interest in enumerate(points_of_interest):
            # Order by the profile
            score[ind] = np.dot(self.profile, point_of_interest.features)
            # Ponderate by the distance
            score[ind] *= self.distance_regularization(point_of_interest.dist(self.mid_point))
            best_pi = np.argsort(score)
        return best_pi[:self.keep_point_interests]
    
    
    
