from fractions import Fraction
from math import copysign, floor


class MapLine:

    def __init__(self, xi = 0, yi = 0, xf = 0, yf = 0):
        ''' Basic line class. '''
        self.x1, self.y1, self.x2, self.y2 = xi, yi, xf, yf

    def getpoint(self, param):
        ''' Returns a point on the line between (x1, y1) and (x2, y2).
        param is a parameter between 0 and 1 inclusive. getPoint(0) returns
        (x1, y1), getPoint(1) returns (x2, y2), and fractional values
        between return a point that fraction of the way on the line. '''
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        return (self.x1 + param * dx, self.y1 + param * dy)
