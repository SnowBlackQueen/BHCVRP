class DistanceNotAccessibleException(Exception):
    def __init__(self, distance=None):
        if distance is not None:
            self.distance = distance
            
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)

    def get_distance(self):
        return getattr(self, 'distance', None)