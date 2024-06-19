class RLC_Exception(Exception):
    def __init__(self, rlc=None):
        if rlc is not None:
            self.rlc = rlc
            
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)

    def get_rlc(self):
        return getattr(self, 'rlc', None)