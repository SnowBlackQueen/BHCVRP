from distance import Distance
import math 

class Haversine(Distance):

    EARTH_RADIUS_KM = 6371

    def __init__(self):
        super().__init__()

    def calculateDistance(self, axis_X_start, axis_Y_start, axis_X_end, axis_Y_end):
        distance = 0.0

        longitude_start = axis_X_start * (math.pi / 180)
        latitude_start = axis_Y_start * (math.pi / 180)

        longitude_end = axis_X_end * (math.pi / 180)
        latitude_end = axis_Y_end * (math.pi / 180)

        dif_latitude = latitude_end - latitude_start
        dif_longitude = longitude_end - longitude_start

        distance = (math.sin(dif_latitude / 2) ** 2 +
                    math.cos(latitude_start) * math.cos(latitude_end) * 
                    (math.sin(dif_longitude / 2) ** 2))
        distance = 2 * self.EARTH_RADIUS_KM * math.atan2(math.sqrt(distance), math.sqrt(1 - distance))

        return distance