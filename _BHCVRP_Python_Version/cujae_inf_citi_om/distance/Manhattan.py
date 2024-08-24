from distance import Distance
import math

class Manhattan(Distance):

    def __init__(self):
        super().__init__()

    def calculateDistance(self, axis_X_start, axis_Y_start, axis_X_end, axis_Y_end):
        distance = 0.0
        axisX = 0.0
        axisY = 0.0

        axisX = abs(axis_X_start - axis_X_end)
        axisY = abs(axis_Y_start - axis_Y_end)
        distance = axisX + axisY

        return distance