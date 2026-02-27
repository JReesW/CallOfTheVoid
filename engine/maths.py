type Point = tuple[float, float]


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end


def clamp(a: float, _min: float, _max: float) -> float:
    return max(_min, min(a, _max))
