from distance.Distance import Distance
from factory.interfaces.DistanceType import DistanceType

# Interface that defines how to create a Distance object
class IFactoryDistance:
    def create_distance(self, distance_type: 'DistanceType') -> Distance:
        pass

