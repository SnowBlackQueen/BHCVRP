from typing import Type
from cujae_inf_citi_om.factory.f_interfaces import DistanceType, IFactoryDistance
from cujae_inf_citi_om.distance import Distance
from cujae_inf_citi_om.factory.f_methods import FactoryLoader
import traceback

class FactoryDistance(IFactoryDistance):
    def createDistance(self, typeDistance: DistanceType) -> Distance:
        class_name = f"cujae_inf_citi_om.distance.{typeDistance}"
        distance = None
        try:
            distance = FactoryLoader.getInstance(class_name)
        except (ClassNotFoundError, ValueError, SecurityError, TypeError, AttributeError, InvocationError) as e:
            traceback.print_exc()
        return distance

