from abc import ABC, abstractmethod
from typing import List
from generator.solution.Route import Route

class StepOptimization(ABC):
    
    @abstractmethod
    def to_optimize(self, route: Route):
        pass
    
    def invert(self, list_candidates: List[int], pos_ini: int, pos_end: int):
        if pos_ini > pos_end:
            pos_ini, pos_end = pos_end, pos_ini
        
        sub_list = list_candidates[pos_ini + 1: pos_end + 1]
        pos_final = len(sub_list)
        
        for j in range(1, (pos_final // 2) + 1):
            value_key_first = sub_list[j - 1]
            list_candidates[j + pos_ini] = list_candidates[pos_end]
            list_candidates[pos_end] = value_key_first
            pos_end -= 1


