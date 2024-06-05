from generator.heuristic import Heuristic
from factory.f_interfaces import HeuristicType

# Interfaz que define como crear un objeto Heuristic

class IFactoryDistance:
    def create_distance(self, distance_type: 'HeuristicType') -> Heuristic:
        pass
