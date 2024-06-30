class WithoutCapacityException(Exception):
    def __init__(self, capacity=None):
        if capacity is not None:
            self.capacity = capacity
        
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)

    def get_capacity(self):
        return getattr(self, 'capacity', None)
