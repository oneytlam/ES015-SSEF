from math import sqrt
# # Dr bui's floor plan
# RIGHT_X_metres = 1330
# BOTTOM_Y_metres = 1090
# RIGHT_X_pixels = 866
# BOTTOM_Y_pixels = 614
# ORIGIN_X, ORIGIN_Y = 0, 0
# dx, dy = 1, 1  # right, down

# yt's floor plan
RIGHT_X_metres = 16
BOTTOM_Y_metres = 18
RIGHT_X_pixels = 800
BOTTOM_Y_pixels = 900
ORIGIN_X, ORIGIN_Y = 100, 800
dx, dy = 1, -1  # right, up

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return (f"({self.x}, {self.y})")

    def dist(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

class Wall:
    def __init__(self, topLeft, bottomRight):
        self.x, self.y = topLeft
        self.width = bottomRight[0] - self.x
        self.height = bottomRight[1] - self.y
        
        # Top left, top right, bottom left, bottom right
        self.points = []
        self.points.append(Point(topLeft[0], topLeft[1]))
        self.points.append(Point(bottomRight[0], topLeft[1]))
        self.points.append(Point(topLeft[0], bottomRight[0]))
        self.points.append(Point(bottomRight[0], bottomRight[1]))
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.width}, {self.height})"
        

def get_walls():
    # wall_coordinates = [[[183, 13], [190, 183]], [[190, 176], [368, 183]], [[334, 183], [340, 207]],
    #                         [[422, 13], [429, 207]], [[419, 259], [429, 283]], [[429, 273], [625, 283]],
    #                         [[616, 42], [625, 273]], [[412, 452], [419, 514]]]
    wall_coordinates = [[[400, 400], [410, 900]], [[500, 490], [800, 500]]]
    
    for i in range(len(wall_coordinates)):
        for j in range(2):
            wall_coordinates[i][j][0] = dx * (wall_coordinates[i][j][0] - ORIGIN_X) / RIGHT_X_pixels * RIGHT_X_metres
            wall_coordinates[i][j][1] = dy * (wall_coordinates[i][j][1] - ORIGIN_Y) / BOTTOM_Y_pixels * BOTTOM_Y_metres
    
    walls = []
    for wall in wall_coordinates:
        walls.append(Wall(wall[0], wall[1]))
        
    return walls

WALLS = get_walls()
        