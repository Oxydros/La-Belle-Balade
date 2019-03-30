#%%
import numpy as np





class PointOfInterest:
    def __init__(self, place_class, coord, rating, n_rating, classes, visiting_time=1800):
        self.place_class = place_class #the classe of the point of interest
        self.coord = coord #the coordinates of the point of interest
        self.visiting_time = visiting_time #the duration of the visit, in seconds
        self.rating = self.get_rating(rating,n_rating)  #the rating of the point of interest, in [0,1]
        self.features = self.features(classes)
    
    def get_rating(self, rating, n_rating):
        if n_rating<1000:
            return 0.1
        else:
            return np.max([rating,0.1])
    
    def dist(self, point):
        x = (point[0]-self.coord[0])*np.cos((point[1]+self.coord[1])/2)
        y = (point[1]-self.coord[1])
        return np.sqrt(x**2 + y**2)*6.371
    
    def features(self, classes):
        features = np.full(len(classes),0.3*self.rating)
        features[np.where(classes==self.place_class)] = self.rating
        return features
    