class Line:
    def __init__(self, m=None, b=None, y=None):
        self.m = m
        self.b = b
        self.y = y

    def parallel(self, line):
        return self.m / self.b == line.m / line.b


def line_from_points(x1, x2, y1, y2):
    return Line((y1 - y2) / (x1 - x2), (x1 * y2 - x2 * y1) / (x1 - x2))
