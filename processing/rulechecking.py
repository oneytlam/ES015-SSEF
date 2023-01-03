# Check if two line segments intersect
def ccw(A,B,C):
    return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

# Return True if intersect
def lineIntersect(coords, prevCoords, p1, p2):
    return ccw(coords, p1, p2) != ccw(prevCoords, p1, p2) and ccw(coords, prevCoords, p1) != ccw(coords, prevCoords, p2)

# Return list of booleans to see which segments are intersected
def checkIntersect(coords, prevCoords, wall):
    topLeft, topRight, bottomLeft, bottomRight = wall.points
    # Check for each line segment - top, bottom, left, right
    checks = [0, 0, 0, 0]
    checks[0] = lineIntersect(coords, prevCoords, topLeft, topRight)
    checks[1] = lineIntersect(coords, prevCoords, bottomLeft, bottomRight)
    checks[2] = lineIntersect(coords, prevCoords, topLeft, bottomLeft)
    checks[3] = lineIntersect(coords, prevCoords, topRight, bottomRight)
    return checks

# def getNewCoords(coords, prevCoords, wall, checks):
    
def validCoords(coords, prevCoords, walls, time_interval, max_speed = 1.3):
    for wall in walls:
        checks = checkIntersect(coords, prevCoords, wall)
        if checks.count(1) == 0:  # No intersect
            pass
        else:
            if time_interval >= 6:
                return [coords.x, coords.y]
            return [prevCoords.x, prevCoords.y]
            # return getNewCoords(coords, prevCoords, wall, checks)
    
    # Check distance
    if coords.dist(prevCoords) > max(max_speed * time_interval, 1.3):
        coords.x = prevCoords.x + 6.5 * (coords.x - prevCoords.x) / coords.dist(prevCoords)
        coords.y = prevCoords.y + 6.5 * (coords.y - prevCoords.y) / coords.dist(prevCoords)
    
    return [coords.x, coords.y]
    
