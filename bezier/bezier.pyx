cpdef list[float] bezier(float t, list p1, list p2):
    cdef list q1 = [0, 0]

    q1[0] = (1 - t) * p1[0] + t * p2[0]
    q1[1] = (1 - t) * p1[1] + t * p2[1]
    
    return q1

cpdef list[list[float]] multi_points(float t, list points):
    
    cdef int i = 0
    cdef list newpoints = []

    for i in range(0, len(points) - 1):
        newpoints += [bezier(t, points[i], points[i + 1])]

    return newpoints

cpdef list[float] single_point(float t, list points):

    cdef list newpoints = points

    while len(newpoints) > 1:
        newpoints = multi_points(t, newpoints)

    return newpoints[0]

cpdef list[list[float]] bezier_curve(list points):
    cdef list curve = []
    cdef list t = [i * 0.01 for i in range(100 + 1)]
    cdef float i

    for i in t:
        curve.append(single_point(i, points))


    return curve

cpdef list[list[float]] split_line(list line):
    cdef list points = [[point.x, point.y] for point in line]
    cdef list new_points = []
    cdef int magic_number = 120
    cdef int magic_number2 = 5
    while len(points):
        if len(points) > magic_number:
            new_points.append(points[:magic_number])
            points = points[magic_number-magic_number2:]
        else:
            if len(new_points):
                for point in points:
                    new_points[-1].append(point)
            else:
                new_points = [points]
            break
    new_points = [bezier_curve(points) for points in new_points]
    return [point for points in new_points for point in points]
