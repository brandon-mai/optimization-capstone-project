"""
CBUS problem:
There are n passengers 1, 2, …, n.
The passenger i want to travel from point i to point i + n (i = 1,2,…,n).
There is a bus located at point 0 and has k places for transporting the passengers
    (it means at any time, there are at most k passengers on the bus).
You are given the distance matrix c in which c(i,j) is the traveling distance
    from point i to point j (i, j = 0,1,…, 2n).
Compute the shortest route for the bus, serving n passengers and coming back to point 0.
Input
    Line 1 contains n and k (1≤n≤1000,1≤k≤50)
    Line i+1 (i=1,2,…,2n+1) contains the (i−1)th line of the matrix c
    (rows and columns are indexed from 0,1,2,..,2n).
Output
    Line 1: write the value n
    Line 2: Write the sequence of points (pickup and drop-off) of passengers
    (separated by a SPACE character)
"""
# Simulated annealing

import time
import math
import random
import NearestNeighbor


def import_data_from_keyboard():
    first_line = input().split()
    n, k = int(first_line[0]), int(first_line[1])
    distance_matrix = []

    for i in range(2 * n + 1):
        temp = input().split()  # new line contains all char element
        next_line = [int(number) for number in temp]
        distance_matrix.append(next_line)

    return n, k, distance_matrix


def import_data_from_file(filename):
    f = open(filename, 'r')

    first_line = f.readline().split()
    n, k = int(first_line[0]), int(first_line[1])
    distance_matrix = []

    for i in range(2 * n + 1):
        temp = f.readline().split()  # new line contains all char element
        next_line = [int(number) for number in temp]
        distance_matrix.append(next_line)

    f.close()

    return n, k, distance_matrix


def generate_initial_solution(n, k, distance_matrix):
    greedy_solver = NearestNeighbor.Solver(n, k, distance_matrix)
    greedy_solver.solve_greedy()
    return greedy_solver.ans[:]


def distance(route, distance_matrix):
    full_route = [0] + route + [0]
    n = len(route) + 1
    dist = 0

    for i in range(n):
        dist += distance_matrix[full_route[i]][full_route[i + 1]]
    return dist


def check(n, k, route):  # checking if the route satisfied the constrains
    capacity = 0
    for point in route:
        capacity = capacity + 1 if point <= n else capacity - 1

        if point <= n:
            if route.index(point) > route.index(point + n):  # passenger i must be on the bus before the drop-off
                return False

        if capacity > k or capacity < 0:
            return False
    return True


# The next 4 function are the 4 methods for generating candidate route
def inverse(route):  # inverses the order of 2 cities in the route
    n = len(route)
    p1, p2 = random.choices(range(n), k=2)
    point1, point2 = min(p1, p2), max(p1, p2)

    new_part = route[point1:point2 + 1]
    new_part = new_part[::-1]

    new_route = route[0:point1] + new_part + route[point2 + 1:n + 1]
    return new_route


def swap(route1):  # swap two arbitrary points
    route = route1[:]
    n = len(route)
    p1, p2 = random.choices(range(n), k=2)
    point1, point2 = min(p1, p2), max(p1, p2)
    route[point1], route[point2] = route[point2], route[point1]

    return route


def insert(route):  # select random point j in the route and insert it to the ith position

    new_route = route[:]
    i, j = random.choices(range(n), k=2)

    if i < j:
        x0 = new_route.pop(i)
        new_route.insert(j, x0)
    else:
        x0 = new_route.pop(i)
        new_route.insert(j + 1, x0)

    return new_route


def swap_routes(route1):  # select a subroute [a:b+1] and insert in at another position
    route = route1[:]
    n = len(route)
    while True:
        point1, point2 = random.choices(range(n), k=2)
        if point1 <= point2: break

    temp = route[point1:point2 + 1]
    del route[point1:point2 + 1]
    insert_position = random.choice(range(n))
    for i in temp:
        route.insert(insert_position, i)
    return route


def get_neighbor(n, k, route1):
    route = list(route1)
    while True:
        func = random.choice([0, 1, 2, 3])
        new_route = []
        if func == 0:
            new_route = inverse(route)
        elif func == 1:
            new_route = insert(route)
        elif func == 2:
            new_route = swap(route)
        else:
            new_route = swap_routes(route)

        if (check(n, k, new_route)):
            return new_route


def Simulated_Annealing(n, k, distance_matrix):
    temperature = 5000
    alpha = 0.99
    time_limit = 180

    shortest_route = generate_initial_solution(n, k, distance_matrix)
    t = time.time()

    while time.time() - t < time_limit:
        # while distance(shortest_route, distance_matrix) >= 128:
        candidate_route = get_neighbor(n, k, shortest_route)

        delta = distance(candidate_route, distance_matrix) - distance(shortest_route, distance_matrix)
        if delta < 0:  # better
            shortest_route = candidate_route
            print("Best result found: ", distance(shortest_route, distance_matrix), "temp = ", temperature)
        else:
            p = math.exp(-delta / temperature)
            r = random.uniform(0, 1)
            if r < p:
                shortest_route = candidate_route
                print("Best result found: ", distance(shortest_route, distance_matrix), "temp = ", temperature)

        temperature *= alpha

    return shortest_route


# N, K, distance_matrix = import_data_from_keyboard()
n, k, distance_matrix = import_data_from_file('dataset/input100.txt')

result = Simulated_Annealing(n, k, distance_matrix)
print(n)
print(result)
print("Best result found: ", distance(result, distance_matrix))

# print(check(n, k, generate_initial_solution(n, k, distance_matrix)))
# print(distance(generate_initial_solution(n, k, distance_matrix), distance_matrix))