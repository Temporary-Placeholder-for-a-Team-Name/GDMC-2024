class Point:
    def __init__(self, x : int = 0, y : int = 0, z : int = 0, p : tuple[int,int,int] = None):
        if p != None: x,y,z = p
        self.x = x
        self.y = y
        self.z = z
        self.position = (x,y,z)
        
    def set_position(self, x : int = None, y : int = None, z : int = None, p : tuple[int,int,int] = None):
        if p != None: x,y,z = p
        self.x = x if x != None else self.x
        self.y = y if y != None else self.y
        self.z = z if z != None else self.z
        self.position = (self.x,self.y,self.z)

    def __eq__(self, other : 'Point') -> bool:
        return self.position == other.position

    def __repr__(self):
        return f"Point({self.position})"

    def __add__(self, other : 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other : 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __floordiv__(self, other : int) -> 'Point':
        return Point(self.x // other, self.y // other, self.z // other)

    def __mul__(self, other : int) -> 'Point':
        return Point(self.x * other, self.y * other, self.z * other)

    def distance(self, other : 'Point', counted_coord=None) -> float:
        if counted_coord is None:
            counted_coord = [1, 1, 1]
        return (((self.x - other.x) ** 2 * counted_coord[0]) + ((self.y - other.y) ** 2 * counted_coord[1]) + ((self.z - other.z) ** 2 * counted_coord[2])) ** 0.5

    """
    offset is a Point
    """
    def to_Vec2iLike(self, offset = None) -> tuple[int,int,int]:
        if not offset:
            return self.x, self.y, self.z
        return self.x + offset.x, self.y + offset.y, self.z + offset.z

    def copy(self) -> 'Point':
        return Point(self.x, self.y, self.z)

    def sign(self):
        return Point(1 if self.x > 0 else -1, 1 if self.y > 0 else -1, 1 if self.z > 0 else -1)

    def scalaire2D(self, other : 'Point') -> int:
        return self.x * other.x + self.z * other.z

    def to_dict(self):
        return {"x": self.x, "y": self.y, "z": self.z}