from cujae_inf_citi_om.distance import Distance
from cujae_inf_citi_om.factory.f_interfaces import DistanceType

# Interface that defines how to create a Distance object
class IFactoryDistance:
    def create_distance(self, distance_type: 'DistanceType') -> Distance:
        pass

