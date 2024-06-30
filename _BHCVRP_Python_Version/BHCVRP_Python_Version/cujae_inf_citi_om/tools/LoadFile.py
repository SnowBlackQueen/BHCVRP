import io
from typing import List
from io import FileIO
from io import StringIO
import re
from data.CustomerType import CustomerType

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
                self.instance_file = [line.strip() for line in file if not self.find_end_element(line)]
            return True
        except IOError as e:
            print(e)
            return False

    def load_count_vehicles_for_depot(self, count_vehicles):
        total_vehicles = self.instance_file[0].split(" ")[0]
        total_depots = self.load_total_depots()
        count_fleet = [total_vehicles]
        count_vehicles.extend([count_fleet] * total_depots)

    def load_count_vehicles_for_depot_ttrp(self, count_vehicles):
        _, _, _, total_vehicles = self.instance_file[0].split(" ", 3)
        total_depots = 1
        count_vehicles.extend([int(total_vehicles)] * total_depots)

    def load_count_trailers_for_depot_ttrp(self, count_trailers):
        _, _, _, _, total_trailers = self.instance_file[0].split(" ", 4)
        total_depots = 1
        count_trailers.extend([int(total_trailers)] * total_depots)

    def load_total_customers(self):
        _, total_customers, *_ = self.instance_file[0].split(" ", 2)
        return int(total_customers)

    def load_total_customers_ttrp(self):
        _, _, total_customers, *_ = self.instance_file[0].split(" ", 3)
        return int(total_customers)

    def load_total_depots(self):
        _, _, total_depots, *_ = self.instance_file[0].split(" ", 3)
        return int(total_depots)

    def is_load_capacity_vehicles(self, capacity_vehicles):
        total_depots = self.load_total_depots()
        for i in range(1, total_depots + 1):
            capacity_fleet = [float(self.instance_file[i].split(" ")[0])]
            capacity_vehicles.append(capacity_fleet)

    def load_capacity_vehicles_ttrp(self, capacity_vehicles):
        total_depots = 1
        for i in range(1, total_depots + 1):
            capacity_vehicles.append(float(self.instance_file[0].split(" ")[0]))

    def load_capacity_trailers_ttrp(self, capacity_trailers):
        total_depots = 1
        for i in range(1, total_depots + 1):
            capacity_trailers.append(float(self.instance_file[0].split(" ")[1]))

    def load_capacity_vehicles_for_hfvrp(self, capacity_vehicles):
        capacity_fleet = list(map(float, self.instance_file[1].split(" ")))
        capacity_vehicles.append(capacity_fleet)

    def is_load_customers(self, id_customers, axis_x_customers, axis_y_customers, request_customers):
        total_customers = self.load_total_customers()
        total_depots = self.load_total_depots()
        for i in range(total_depots + 1, total_customers + total_depots + 1):
            tokens = re.split(r'\s+', self.instance_file[i])
            id_customers.append(int(tokens[0]))
            axis_x_customers.append(float(tokens[1]))
            axis_y_customers.append(float(tokens[2]))
            request_customers.append(float(tokens[3]))

    def load_customers_ttrp(self, id_customers, axis_x_customers, axis_y_customers, request_customers, type_customers):
        total_customers = self.load_total_customers_ttrp()
        total_depots = 1
        for i in range(total_depots + 1, total_customers + total_depots + 1):
            id_customer, axis_x, axis_y, request, type_customer = self.instance_file[i].split(" ", 4)
            id_customers.append(int(id_customer))
            axis_x_customers.append(float(axis_x))
            axis_y_customers.append(float(axis_y))
            request_customers.append(float(request))
            type_customers.append(int(type_customer))

    def is_load_depots(self, id_depots, axis_x_depots, axis_y_depots):
        total_customers = self.load_total_customers()
        total_depots = self.load_total_depots()
        for i in range(total_depots + total_customers + 1, len(self.instance_file)):
            tokens = re.split(r'\s+', self.instance_file[i])
            id_depots.append(int(tokens[0]))
            axis_x_depots.append(float(tokens[1]))
            axis_y_depots.append(float(tokens[2]))

    def load_depots_ttrp(self, id_depots, axis_x_depots, axis_y_depots):
        id_depot, axis_x, axis_y, *_ = self.instance_file[1].split(" ", 3)
        id_depots.append(int(id_depot))
        axis_x_depots.append(float(axis_x))
        axis_y_depots.append(float(axis_y))

    def calculate_distance(self, axis_x_start, axis_y_start, axis_x_end, axis_y_end):
        axis_x = (axis_x_start - axis_x_end) ** 2
        axis_y = (axis_y_start - axis_y_end) ** 2
        distance = (axis_x + axis_y) ** 0.5
        return distance

    def fill_list_distances(self, id_customers, axis_x_customers, axis_y_customers, id_depots, axis_x_depots, axis_y_depots, list_distances):
        total_customers = len(id_customers)
        total_depots = len(id_depots)
        for i in range(total_customers):
            distances_from_customers = [self.calculate_distance(axis_x_customers[j], axis_y_customers[j], axis_x_customers[i], axis_y_customers[i]) for j in range(total_customers)]
            for k in range(total_depots):
                distances_from_customers.append(self.calculate_distance(axis_x_depots[k], axis_y_depots[k], axis_x_customers[i], axis_y_customers[i]))
            list_distances.append(distances_from_customers)

        for i in range(total_depots):
            distances_from_customers = [self.calculate_distance(axis_x_customers[j], axis_y_customers[j], axis_x_depots[i], axis_y_depots[i]) for j in range(total_customers)]
            for k in range(total_depots):
                distances_from_customers.append(self.calculate_distance(axis_x_depots[k], axis_y_depots[k], axis_x_depots[i], axis_y_depots[i]))
            list_distances.append(distances_from_customers)
            
    def load_count_vehicles_fleet(self, instance_file):
        fleet = FleetAux()
        tokens = instance_file[0].split(" ")
        fleet.set_count_vehicles(int(tokens[0]))
        return fleet

    def load_count_vehicles_ttrp_fleet(self, instance_file):
        fleet = FleetTTRPAux()
        tokens = instance_file[0].split(" ")
        tokens.pop(0)  # Remove the first token since it's not needed
        tokens.pop(0)  # Remove the second token since it's not needed
        tokens.pop(0)  # Remove the third token since it's not needed
        fleet.set_count_vehicles(int(tokens[0]))
        fleet.set_count_trailers(int(tokens[1]))  # Adjusted for Python naming convention
        return fleet

    def load_count_customers(self, instance_file):
        tokens = instance_file[0].split(" ")
        return int(tokens[1])

    def load_count_depots(self, instance_file):
        tokens = instance_file[0].split(" ")
        tokens.pop(0)  # Remove the first token since it's not needed
        tokens.pop(0)  # Remove the second token since it's not needed
        return int(tokens[1])

    def load_capacity_vehicles(self, instance_file):
        capacities = []
        for i in range(1, len(instance_file)):
            tokens = instance_file[i].split(" ")
            capacities.append(float(tokens[0]))
        return capacities

    def load_customers(self, instance_file):
        customers = []
        for i in range(len(instance_file) - 1, -1, -1):  # Start from end to avoid overlap with depots
            tokens = instance_file[i].split(" ")
            customer = CustomerAux()
            customer.set_id_customer(int(tokens[0]))
            customer.set_axis_x(float(tokens[1]))  # Adjusted for Python naming convention
            customer.set_axis_y(float(tokens[2]))  # Adjusted for Python naming convention
            customer.set_request_customer(float(tokens[3]))  # Adjusted for Python naming convention
            customers.append(customer)
        return customers

    def load_customers_ttrp(self, instance_file):
        customers = []
        for i in range(len(instance_file) - 1, -1, -1):  # Start from end to avoid overlap with depots
            tokens = instance_file[i].split(" ")
            customer = CustomerTTRPAux()
            customer.set_id_customer(int(tokens[0]))
            customer.set_axis_x(float(tokens[1]))  # Adjusted for Python naming convention
            customer.set_axis_y(float(tokens[2]))  # Adjusted for Python naming convention
            customer.set_request_customer(float(tokens[3]))  # Adjusted for Python naming convention
            customer.set_type_customer(int(tokens[4]))  # Adjusted for Python naming convention
            customers.append(customer)
        return customers

    def load_depots(self, instance_file):
        depots = []
        for i in range(len(instance_file) - 1, -1, -1):  # Start from end to avoid overlap with fleets
            tokens = instance_file[i].split(" ")
            depot = DepotAux()
            depot.set_id_depot(int(tokens[0]))  # Adjusted for Python naming convention
            depot.set_axis_x(float(tokens[1]))  # Adjusted for Python naming convention
            depot.set_axis_y(float(tokens[2]))  # Adjusted for Python naming convention
            depots.append(depot)
        capacities = self.load_capacity_vehicles(instance_file)
        for depot, capacity in zip(depots, capacities):
            fleet = self.load_count_vehicles_fleet(instance_file)
            fleet.set_capacity_vehicle(capacity)
            depot.set_list_fleets([fleet])  # Assuming set_listfleets accepts a list
        return depots

class CustomerAux:
    def __init__(self):
        # No parameters needed for default constructor
        self.id_customer = None
        self.request_customer = None
        self.axis_x = None
        self.axis_y = None

    def __init__(self, id_customer, request_customer, axis_x, axis_y):
        self.id_customer = id_customer
        self.request_customer = request_customer
        self.axis_x = axis_x
        self.axis_y = axis_y

    def get_id_customer(self):
        return self.id_customer

    def set_id_customer(self, id_customer):
        self.id_customer = id_customer

    def get_request_customer(self):
        return self.request_customer

    def set_request_customer(self, request_customer):
        self.request_customer = request_customer

    def get_axis_x(self):
        return self.axis_x

    def set_axis_x(self, axis_x):
        self.axis_x = axis_x

    def get_axis_y(self):
        return self.axis_y

    def set_axis_y(self, axis_y):
        self.axis_y = axis_y
        
class CustomerTTRPAux(CustomerAux):
    def __init__(self, type_customer=CustomerType.VC):
        super().__init__()  # Assuming CustomerAux has been defined above
        self.type_customer = type_customer

    def get_type_customer(self):
        return self.type_customer

    def set_type_customer(self, type_customer):
        self.type_customer = type_customer

    def set_type_customer_int(self, type_customer_int):
        if type_customer_int == CustomerType.VC:
            self.type_customer = CustomerType.VC
        elif type_customer_int == CustomerType.TC:
            self.type_customer = CustomerType.TC
        else:
            raise ValueError("Invalid customer type integer")
        
class DepotAux:
    def __init__(self, id_depot=None, list_fleets=None, axis_x=None, axis_y=None):
        self.id_depot = id_depot
        self.list_fleets = list_fleets if list_fleets is not None else []
        self.axis_x = axis_x
        self.axis_y = axis_y

    def get_list_fleets(self):
        return self.list_fleets

    def set_list_fleets(self, list_fleets):
        self.list_fleets = list_fleets

    def get_id_depot(self):
        return self.id_depot

    def set_id_depot(self, id_depot):
        self.id_depot = id_depot

    def get_axis_x(self):
        return self.axis_x

    def set_axis_x(self, axis_x):
        self.axis_x = axis_x

    def get_axis_y(self):
        return self.axis_y

    def set_axis_y(self, axis_y):
        self.axis_y = axis_y
        
class FleetAux:
    def __init__(self, count_vehicles=None, capacity_vehicle=None):
        self.count_vehicles = count_vehicles
        self.capacity_vehicle = capacity_vehicle

    def get_count_vehicles(self):
        return self.count_vehicles

    def set_count_vehicles(self, count_vehicles):
        self.count_vehicles = count_vehicles

    def get_capacity_vehicle(self):
        return self.capacity_vehicle

    def set_capacity_vehicle(self, capacity_vehicle):
        self.capacity_vehicle = capacity_vehicle
        
class FleetTTRPAux(FleetAux):
    def __init__(self, count_trailers=None, capacity_trailer=None):
        super().__init__(count_vehicles=0, capacity_vehicle=0)  # Initialize FleetAux attributes
        self.count_trailers = count_trailers
        self.capacity_trailer = capacity_trailer

    def get_count_trailers(self):
        return self.count_trailers

    def set_count_trailers(self, count_trailers):
        self.count_trailers = count_trailers

    def get_capacity_trailer(self):
        return self.capacity_trailer

    def set_capacity_trailer(self, capacity_trailer):
        self.capacity_trailer = capacity_trailer