from typing import Type
from cujae_inf_citi_om.factory.interfaces import DistanceType, IFactoryDistance
from cujae_inf_citi_om.distance import Distance
from cujae_inf_citi_om.factory.methods import FactoryLoader
import traceback

class FactoryDistance(IFactoryDistance):
    def createDistance(self, type_distance: DistanceType) -> Distance:
        class_name = f"cujae_inf_citi_om.distance.{type_distance}"
        distance = None
        try:
            distance = FactoryLoader.get_instance(class_name)
        except (ModuleNotFoundError, ValueError, PermissionError, FileNotFoundError, TypeError, AttributeError) as e:
            traceback.print_exc()
        return distance

