from typing import Type
from factory.interfaces.DistanceType import DistanceType
from factory.interfaces.IFactoryDistance import IFactoryDistance
from distance.Distance import Distance
from factory.methods.FactoryLoader import FactoryLoader
import traceback

class FactoryDistance(IFactoryDistance):
    def create_distance(self, type_distance: DistanceType) -> Distance:
        class_name = f"distance.{type_distance.name}.{type_distance.name}"
        distance = None
        try:
            distance = FactoryLoader.get_instance(class_name)
        except (ModuleNotFoundError, ValueError, PermissionError, FileNotFoundError, TypeError, AttributeError) as e:
            traceback.print_exc()
        return distance

