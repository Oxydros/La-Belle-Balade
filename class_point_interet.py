import numpy as np





class PointOfInterest:
    def __init__(self, place_class, coord, rating, n_rating, classes):
        self.place_class = place_class
        self.coord = coord
        self.rating = self.get_rating(rating,n_rating)
        self.features = self.features(classes)
    
    def get_rating(self, rating, n_rating):
        if n_rating<1000:
            return 0.1
        else:
            return rating
    
    def dist(self, point):
        x = (point[0]-self.coord[0])*np.cos((point[1]+self.coord[1])/2)
        y = (point[1]-self.coord[1])
        return np.sqrt(x**2 + y**2)*6.371
    
    def features(self, classes):
        features = np.full(len(classes),0.3*rating)
        features[np.where(classes==self.place_class)] = rating
        return features
    