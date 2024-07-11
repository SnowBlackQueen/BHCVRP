class Metric:
    def __init__(self, id_element=None, insertion_cost=None, index=None):
        self._id_element = id_element
        self._insertion_cost = insertion_cost
        self._index = index

    def get_id_element(self):
        return self._id_element

    def set_id_element(self, id_element):
        self._id_element = id_element

    def get_insertion_cost(self):
        return self._insertion_cost

    def set_insertion_cost(self, insertion_cost):
        self._insertion_cost = insertion_cost

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index
