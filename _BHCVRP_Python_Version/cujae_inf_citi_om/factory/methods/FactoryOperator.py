from typing import Type
from cujae_inf_citi_om.factory.interfaces import OperatorType, IFactoryOperator
from cujae_inf_citi_om.generator.postoptimization import StepOptimization
from cujae_inf_citi_om.factory.methods import FactoryLoader
import traceback

class FactoryDistance(IFactoryOperator):
    def createDistance(self, type_operator: OperatorType) -> StepOptimization:
        class_name = f"cujae_inf_citi_om.generator.postoptimization.{type_operator}"
        operator = None
        try:
            operator = FactoryLoader.get_instance(class_name)
        except (ModuleNotFoundError, ValueError, PermissionError, FileNotFoundError, TypeError, AttributeError) as e:
            traceback.print_exc()
        return operator