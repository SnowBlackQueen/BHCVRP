class VehicleSpeedException(Exception):
    def __init__(self, vehicle_speed=None):
        if vehicle_speed is not None:
            self.vehicle_speed = vehicle_speed

    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)

    def get_vehicle_speed(self):
        return getattr(self, "vehicle_speed", None)
