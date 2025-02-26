class BusStopCapacityException(Exception):
    def __init__(self, capacity_bus_stop=None):
        if capacity_bus_stop is not None:
            self.request = capacity_bus_stop

    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)

    def get_capacity_bus_stop(self):
        return getattr(self, "capacity_bus_stop", None)