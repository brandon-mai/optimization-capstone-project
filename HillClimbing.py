import time
import NearestNeighbor

# IMPROVEMENT OF NEAREST NEIGHBOR, BY TRYING TO SWAP PAIRS OF NODES AND GETTING THE BEST ONE


def import_data_input():
    N, K = map(int, input().split())
    distance_matrix = [[int(x) for x in input().split()] for _ in range(2 * N + 1)]
    return N, K, distance_matrix


def import_data_file(file_name):
    with open(file_name, 'r') as f:
        N, K = map(int, f.readline().split())
        distance_matrix = [[int(x) for x in f.readline().split()] for _ in range(2 * N + 1)]
    return N, K, distance_matrix


class Solver:
    def __init__(self, N, K, distance_matrix):
        self.N = N
        self.K = K
        self.Num_Nodes = 2 * N + 1
        self.Distance_Matrix = distance_matrix

        self.ans = list()
        self.best_dist = 0
        self.time = time.time()

    def get_distance(self, route):
        """Return total distance of route."""
        route = [0] + route + [0]
        return sum(self.Distance_Matrix[i][j] for i, j in zip(route, route[1:]))

    def get_first_solution(self):
        """Add initial solution to current best answer/distance with Nearest Neighbor (greedy) algorithm."""
        greedy_solver = NearestNeighbor.Solver(self.N, self.K, self.Distance_Matrix)
        greedy_solver.solve_greedy()
        self.ans = greedy_solver.ans[:]
        self.best_dist = greedy_solver.best_dist

    def validate_route(self, route):
        """Return True if route satisfies constraints."""
        capacity = 0
        for node in route:
            capacity += 1 if node <= self.N else -1

            if node <= self.N:
                if route.index(node) > route.index(node + self.N):
                    return False

            if capacity > self.K or capacity < 0:
                return False

        return True

    def reverse_segment(self, route, i, j):
        """Reverse segment from index i to index j in route."""
        new_route = route[:]
        n = len(route)
        segment_size = (n + j - i + 1) % n
        left = i
        right = j

        for k in range(segment_size // 2):
            new_route[left], new_route[right] = new_route[right], new_route[left]
            left = (left + 1) % segment_size
            right = (segment_size + right - 1) % segment_size

        return new_route

    def node_shift(self, route, i, j):
        """Shift node from index i to between j and j + 1 in route."""
        new_route = route[:]

        if i < j:
            x0 = new_route.pop(i)
            new_route.insert(j, x0)
        else:
            x0 = new_route.pop(i)
            new_route.insert(j + 1, x0)

        return new_route

    def get_neighborhood(self, route, opt='2', time_limit=None):
        """Return a list of neighbors of route, in ascending order of total distance, using 2 or 2.5-opt."""
        neighbor_list = list()
        route = [0] + route
        num_nodes = len(route)

        for i in range(num_nodes - 3):
            x1 = route[i]
            x2 = route[(i + 1) % num_nodes]
            radius = self.Distance_Matrix[x1][x2]

            if i == 0:
                j_max = num_nodes - 2
            else:
                j_max = num_nodes - 1

            for j in range(i + 2, j_max):
                y1 = route[j]
                y2 = route[(j + 1) % num_nodes]

                if time_limit:
                    if time.time() - self.time > time_limit:
                        return sorted(neighbor_list, key=lambda x: self.get_distance(x))

                if self.Distance_Matrix[x1][x2] + self.Distance_Matrix[y1][y2] > self.Distance_Matrix[x1][y1] + \
                        self.Distance_Matrix[x2][y2]:
                    neighbor = self.reverse_segment(route, i, j)
                    neighbor = neighbor[neighbor.index(0):] + neighbor[:neighbor.index(0)]
                    neighbor = neighbor[1:]
                    if self.validate_route(neighbor):
                        neighbor_list.append(neighbor)

                if opt == '2.5':
                    # Look forward, shift x2 to after y1
                    x3 = route[(i + 2) % num_nodes]
                    if x3 != y1:
                        if self.Distance_Matrix[x1][x2] + self.Distance_Matrix[x2][x3] + \
                                self.Distance_Matrix[y1][y2] > self.Distance_Matrix[x1][x3] + \
                                self.Distance_Matrix[y1][x2] + self.Distance_Matrix[x2][y2]:
                            neighbor = self.node_shift(route, (i + 1) % num_nodes, j)
                            neighbor = neighbor[neighbor.index(0):] + neighbor[:neighbor.index(0)]
                            neighbor = neighbor[1:]
                            if self.validate_route(neighbor):
                                neighbor_list.append(neighbor)

                    # Look backward, shift y1 to after x1
                    y0 = route[(num_nodes + j - 1) % num_nodes]
                    if y0 != x2:
                        if self.Distance_Matrix[y0][y1] + self.Distance_Matrix[y1][y2] + \
                                self.Distance_Matrix[x1][x2] > self.Distance_Matrix[y0][y2] + \
                                self.Distance_Matrix[x1][y1] + self.Distance_Matrix[y1][x2]:
                            neighbor = self.node_shift(route, j, i)
                            neighbor = neighbor[neighbor.index(0):] + neighbor[:neighbor.index(0)]
                            neighbor = neighbor[1:]
                            if self.validate_route(neighbor):
                                neighbor_list.append(neighbor)

        return sorted(neighbor_list, key=lambda x: self.get_distance(x))

    def solve_hill_climbing(self, opt='2'):
        """Solve the problem using Local Hill Climbing algorithm."""
        self.time = time.time()
        self.get_first_solution()
        neighborhood = self.get_neighborhood(self.ans, opt=opt)

        while neighborhood:
            neighbor = neighborhood.pop(0)
            neighbor_dist = self.get_distance(neighbor)
            if neighbor_dist < self.best_dist:
                self.ans = neighbor[:]
                self.best_dist = neighbor_dist
                neighborhood = self.get_neighborhood(self.ans, opt=opt)
            else:
                break

    def print_solution(self):
        print(self.N)
        print(*self.ans)
        print(f'\nBest distance found: {self.best_dist}')
        print(f'Time taken: {time.time() - self.time}')


def main():
    # N, K, distance_matrix = import_data_input()
    N, K, distance_matrix = import_data_file('dataset/input100.txt')

    sol = Solver(N, K, distance_matrix)
    sol.solve_hill_climbing(opt='2.5')
    sol.print_solution()


if __name__ == "__main__":
    main()

