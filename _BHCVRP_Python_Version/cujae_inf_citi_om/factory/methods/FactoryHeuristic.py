from typing import Type
from cujae_inf_citi_om.factory.interfaces import HeuristicType, IFactoryHeuristic
from cujae_inf_citi_om.generator.heuristic import Heuristic
from cujae_inf_citi_om.factory.methods import FactoryLoader
import traceback

class FactoryHeuristic(IFactoryHeuristic):
    def createHeuristic(self, type_heuristic: HeuristicType) -> Heuristic:
        class_name = f"cujae_inf_citi_om.distance.{type_heuristic}"
        heuristic = None
        try:
            heuristic = FactoryLoader.get_instance(class_name)
        except (ModuleNotFoundError, ValueError, PermissionError, FileNotFoundError, TypeError, AttributeError) as e:
            traceback.print_exc()
        return heuristic
