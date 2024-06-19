class RequestException(Exception):
    def __init__(self, request=None):
        if request is not None:
            self.request = request
        
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)

    def get_request(self):
        return getattr(self, 'request', None)