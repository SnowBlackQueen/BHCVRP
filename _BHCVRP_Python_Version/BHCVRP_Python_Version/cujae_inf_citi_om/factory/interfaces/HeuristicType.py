from enum import Enum

# Enumerado que indica los tipos de heurísticas de construcción

class HeuristicType(Enum):
    CMT = 0
    KilbyAlgorithm = 1
    MatchingBasedSavingAlgorithm = 2
    MoleJameson = 3
    NearestNeighborWithRLC = 4
    RandomMethod = 5
    SaveParallel = 6
    SaveSequential = 7
    Sweep = 8
    