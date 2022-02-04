from math import *


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, v):
        return Vector2(self.x+v.x, self.y+v.y)

    def sub(self, v):
        return Vector2(self.x-v.x, self.y-v.y)

    def magnitude(self):
        return sqrt(self.x**2+self.y**2)

    def multiply(self, n):
        return Vector2(self.x*n, self.y*n)

