
import journey_optimization
import class_point_interest
import User
import numpy as np

classes = ["musée","parc"]

u = User.User(np.array([0.1,0.2]),(1,2),(4,5),2000000,keep_point_interests=3)
points_of_interest = [class_point_interest.PointOfInterest("musée", (2,3), 1.0, 1001, classes),\
                       class_point_interest.PointOfInterest("parc", (4,3), 1.0, 1001, classes),\
                       class_point_interest.PointOfInterest("musée", (6,6), 1.0, 1001, classes),
                       class_point_interest.PointOfInterest("parc", (7,6), 1.0, 1001, classes)]
arg_interest = u.find_relevant_interest_points(points_of_interest)
keep_points_interest = [points_of_interest[elem] for elem in arg_interest]
j = journey_optimization.Journey(u,keep_points_interest)
j_opt = j.get_optimal_journey()