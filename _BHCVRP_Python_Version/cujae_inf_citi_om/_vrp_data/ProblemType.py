from enum import Enum

# Enumerado que indica los tipos de problemas VRP.

class ProblemType(Enum):
    
    CVRP = 0
    HFVRP = 1
    MDVRP = 2
    OVRP = 3
    TTRP = 4