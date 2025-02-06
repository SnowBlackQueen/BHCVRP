class TimeWindowException(Exception):
    def __init__(self, time_window=None):
        if time_window is not None:
            self.initial_node = time_window
            self.end_node = time_window

    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)

    def get_initial_node(self):
        return getattr(self, "time_window", None)

    def get_end_node(self):
        return getattr(self, "time_window", None)