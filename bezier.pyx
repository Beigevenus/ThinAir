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