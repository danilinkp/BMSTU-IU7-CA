from typing import List, Optional

type Points = List[Point]


class Point:
    def __init__(self, x: float, y: float, z: Optional[float], p: float):
        self.x = x
        self.y = y
        self.z = z
        self.p = p

    def __str__(self):
        return f"{self.x} {self.y} {self.z} {self.p}"
