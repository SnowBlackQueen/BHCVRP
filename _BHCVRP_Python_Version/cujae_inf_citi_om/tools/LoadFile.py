import io
from typing import List
from io import LineIO
from io import StringIO
import re

class LoadFile:
    def __init__(self):
        self.instance_file = []

    def get_instance_file(self) -> List[str]:
        return self.instance_file

    def set_instance_file(self, instance_file: List[str]) -> None:
        self.instance_file = instance_file

    def find_end_element(self, lines: str) -> bool:
        return "EOF" in lines

    def load_file(self, path_file: str) -> bool:
        try:
            with open(path_file, 'r') as file:
                self.instanceFile = file.readlines()
                return True
        except FileNotFoundError:
            return False

    def load_count_vehicles_for_depot(self, count_vehicles: List[List[int]]) -> None:
        if self.instanceFile:
            total_vehicles = int(self.instanceFile[0].split()[0])
            total_depots = self.load_total_depots()  # Implement loadTotalDepots() method

            count_fleet = [total_vehicles]

            for _ in range(total_depots):
                count_vehicles.append(count_fleet)

    def load_count_vehicles_for_depot_ttrp(self, count_vehicles: List[int]) -> None:
        if self.instanceFile:
            line = self.instanceFile[0]
            tokens = re.split(r'\s+', line)
            total_vehicles = int(tokens[3])  # Assuming the format is consistent
            count_vehicles.extend([total_vehicles] * 1)  # Total depots is 1

    def load_count_trailers_for_depot_ttrp(self, count_trailers: List[int]) -> None:
        if self.instanceFile:
            line = self.instanceFile[0]
            tokens = re.split(r'\s+', line)
            total_trailers = int(tokens[4])  # Assuming the format is consistent
            count_trailers.extend([total_trailers] * 1)  # Total depots is 1

    def load_total_customers(self) -> int:
        if self.instanceFile:
            line = self.instanceFile[0]
            tokens = re.split(r'\s+', line)
            return int(tokens[2])  # Assuming the format is consistent

    def load_total_customers_ttrp(self) -> int:
        if self.instanceFile:
            line = self.instanceFile[0]
            tokens = re.split(r'\s+', line)
            return int(tokens[3])  # Assuming the format is consistent

    def load_total_depots(self) -> int:
        if self.instanceFile:
            line = self.instanceFile[0]
            tokens = re.split(r'\s+', line)
            return int(tokens[2])  # Assuming the format is consistent
        
    def load_capacity_vehicles(self, capacity_vehicles):
        total_depots = self.load_total_depots()
    
        for i in range(1, total_depots + 1):
            tool = self.instance_file[i].split(" ")
            capacity_fleet = [float(tool[0])]
            capacity_vehicles.append(capacity_fleet)

    def load_capacity_vehicles_ttrp(self, capacity_vehicles):
        total_depots = 1
        
        for i in range(1, total_depots + 1):
            tool = self.instance_file[0].split(" ")
            capacity_vehicles.append(float(tool[0]))

    def load_capacity_trailers_ttrp(self, capacity_trailers):
        total_depots = 1
        
        for i in range(1, total_depots + 1):
            tool = self.instance_file[0].split(" ")
            tool[0]  # Ignore the first token
            capacity_trailers.append(float(tool[1]))

    def load_capacity_vehicles_for_hfvrp(self, capacity_vehicles):
        tool = self.instance_file[1].split(" ")
        capacity_fleet = [float(token) for token in tool]
        capacity_vehicles.append(capacity_fleet)
    
    def load_customers(self, id_customers, axis_x_customers, axis_y_customers, request_customers):
        total_customers = self.load_total_customers()
        total_depots = self.load_total_depots()
        
        for i in range(self, total_depots + 1, total_customers + total_depots + 1):
            tool = self.instance_file[i].split(" ")
            id_customers.append(int(tool[0]))
            axis_x_customers.append(float(tool[1]))
            axis_y_customers.append(float(tool[2]))
            request_customers.append(float(tool[3]))

    def load_customers_ttrp(self, id_customers, axis_x_customers, axis_y_customers, request_customers, type_customers):
        total_customers = self.load_total_customers_ttrp()
        total_depots = 1
        
        for i in range(total_depots + 1, total_customers + total_depots + 1):
            tool = self.instance_file[i].split(" ")
            id_customers.append(int(tool[0]))
            axis_x_customers.append(float(tool[1]))
            axis_y_customers.append(float(tool[2]))
            request_customers.append(float(tool[3]))
            type_customers.append(int(tool[4]))

    def load_depots(self, id_depots, axis_x_depots, axis_y_depots):
        total_customers = self.load_total_customers()
        total_depots =self.load_total_depots()
        
        for i in range(total_depots + total_customers + 1, len(self.instance_file)):
            tool = self.instance_file[i].split(" ")
            id_depots.append(int(tool[0]))
            axis_x_depots.append(float(tool[1]))
            axis_y_depots.append(float(tool[2]))