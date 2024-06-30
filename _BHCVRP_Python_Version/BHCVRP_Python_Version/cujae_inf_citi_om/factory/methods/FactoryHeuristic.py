from typing import Type
from factory.interfaces.HeuristicType import HeuristicType
from factory.interfaces.IFactoryHeuristic import IFactoryHeuristic
from generator.heuristic.Heuristic import Heuristic
from factory.methods.FactoryLoader import FactoryLoader
import traceback

class FactoryHeuristic(IFactoryHeuristic):
    def create_heuristic(self, type_heuristic: HeuristicType) -> Heuristic:
        class_name = f"generator.heuristic.{type_heuristic.name}"
        heuristic = None
        try:
            heuristic = FactoryLoader.get_instance(class_name)
        except (ModuleNotFoundError, ValueError, PermissionError, FileNotFoundError, TypeError, AttributeError) as e:
            traceback.print_exc()
        return heuristic
