from enum import Enum

# Enumerado que indica los tipos de heurísticas de construcción

class HeuristicType(Enum):
    CMT = 0
    KilbyAlgorithm = 1
    MoleJameson = 2
    NearestNeighborWithRLC = 3
    RandomMethod = 4
    SaveParallel = 5
    SaveSequential = 6
    Sweep = 7
    