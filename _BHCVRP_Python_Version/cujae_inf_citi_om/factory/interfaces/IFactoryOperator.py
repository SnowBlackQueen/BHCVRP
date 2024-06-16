from cujae_inf_citi_om.generator.postoptimization import StepOptimization
from cujae_inf_citi_om.factory.interfaces import OperatorType

# Interface that defines how to create a Distance object
class IFactoryOperator:
    def create_operator(self, operator_type: 'OperatorType') -> StepOptimization:
        pass