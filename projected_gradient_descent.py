import numpy as np

# import matplotlib.pyplot as plt
# from matplotlib.patches import Circle, Wedge, Polygon
# from matplotlib.collections import PatchCollection, LineCollection

X = [[(0, 0), (3, 0)],
     [(3, 0), (3, 1)],
     [(3, 1), (1.5, 2.5)],
     [(1.5, 2.5), (0, 2.5)],
     [(0, 2.5), (0, 0)]]


def ccw(point1, point2, point3):
    def rise(start, end):
        return start[1] - end[1]

    def run(start, end):
        return start[0] - end[0]

    return rise(point1, point2) * run(point2, point3) - \
           run(point1, point2) * rise(point2, point3)


def is_point_inside_convex_polygon(point, segments):
    orientation = [ccw(point, seg_start, seg_end) > 0 for seg_start, seg_end in segments]
    print(orientation)
    return (False in orientation) ^ (True in orientation)


def project_on_line(point, line_start, line_end):
    norm = sum([(line_start[i] - line_end[i]) ** 2 for i in [0, 1]])
    cofact = sum([(point[i] - line_start[i]) * (line_end[i] - line_start[i]) for i in [0, 1]])
    return np.array([line_start[i] + cofact * (line_end[i] - line_start[i]) / norm for i in [0, 1]])


def project_on_box(point, min_x, max_x, min_y, max_y):
    return np.array([min(max(point[0], min_x), max_x), min(max(point[1], min_y), max_y)])


def project_on_set(point, X):
    x, y = point[0], point[1]

    if is_point_inside_convex_polygon(point, X):
        return point
    if y >= 1 and y - x <= -2:
        return np.array([3, 1])
    elif x >= 1.5 and y - x >= 1:
        return np.array([1.5, 2.5])
    elif -2 < (y - x) < 1 and x + y > 4:
        return project_on_line(point, line_start=(1, 3), line_end=(1.5, 2.5))
    elif x < 1.5 or y < 1:
        return project_on_box(point, min_x=0, max_x=3, min_y=0, max_y=2.5)
    else:
        print("THIS SHOULD NOT HAPPEN")


def descent(point, gradient, learning_rate):
    new_point = point - learning_rate * gradient(point)
    return project_on_set(new_point, X)


def main():
    start = np.array([2.5, 1])
    learning_rate = 0.05

    def gradient(point):
        return np.array([2 * point[0] - 4, 8 * point[1] - 28])

    current = start
    for _ in range(5):
        current = descent(current, gradient, learning_rate)
        print("Grad Descent: " + str(current))


if "__name__" == "__main__":
    main()

main()
