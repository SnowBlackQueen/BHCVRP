class CostException(Exception):
    def __init__(self, cost=None):
        if cost is not None:
            self.request = cost
        
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)

    def get_cost(self):
        return getattr(self, 'cost', None)