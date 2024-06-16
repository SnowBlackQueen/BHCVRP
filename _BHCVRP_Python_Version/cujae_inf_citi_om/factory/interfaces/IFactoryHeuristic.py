from generator.heuristic import Heuristic
from factory.interfaces import HeuristicType

# Interfaz que define como crear un objeto Heuristic

class IFactoryHeuristic:
    def create_heuristic(self, heuristic_type: 'HeuristicType') -> Heuristic:
        pass
