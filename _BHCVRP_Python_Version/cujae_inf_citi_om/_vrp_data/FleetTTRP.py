from _vrp_data import Fleet

# Clase que modela los datos de una flota en el TTRP

class FleetTTRP(Fleet):
    
    def __init__(self, count_trailers, capacity_trailer):
        super().__init__()
        self._count_trailers = count_trailers
        self._capacity_trailer = capacity_trailer

    def get_count_trailers(self):
        return self._count_trailers

    def set_count_trailers(self, count_trailers):
        self._count_trailers = count_trailers

    def get_capacity_trailer(self):
        return self._capacity_trailer

    def set_capacity_trailer(self, capacity_trailer):
        self._capacity_trailer = capacity_trailer