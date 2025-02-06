class ServiceTimeException(Exception):
    def __init__(self, service_time=None):
        if service_time is not None:
            self.service_time = service_time

    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)

    def get_service_time(self):
        return getattr(self, "service_time", None)