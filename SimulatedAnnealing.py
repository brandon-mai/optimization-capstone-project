import time
import math
import random
import NearestNeighbor

# CLASSIC SIMULATED ANNEALING ALGORITHM


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
        self.ans = greedy_solver.ans
        self.best_dist = greedy_solver.best_dist

    def validate_route(self, route):
        """Return True if route satisfies constraints."""
        capacity = 0
        for node in route:
            capacity += 1 if node <= self.N else -1

            if node <= self.N:
                if route.index(node) > route.index(node + self.N):
                    return 0

            if capacity > self.K or capacity < 0:
                return 0

        return 1

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

    def adjacent_swap(self, route, i, j):
        """Swap 4 adjacent nodes in route."""
        new_route = route[:]
        new_route[i], new_route[i + 1] = new_route[i + 1], new_route[i]
        new_route[j], new_route[j + 1] = new_route[j + 1], new_route[j]
        return new_route

    def get_random_neighbor(self, route):
        """Return a satisfying neighbor by various mutating methods."""
        while True:
            i, j = random.sample(range(1, self.Num_Nodes - 2), 2)
            mutation = random.choice([self.node_shift, self.adjacent_swap, self.reverse_segment])
            new_route = mutation(route, i, j)

            if self.validate_route(new_route):
                return new_route

    def solve_simulated_annealing(self, initial_temp=5000, alpha=0.99, time_limit=30):
        """Solve the problem using Simulated Annealing algorithm."""
        self.time = time.time()
        self.get_first_solution()

        temp = initial_temp

        best_ans = self.ans[:]
        best_dist = self.best_dist

        current_ans = best_ans[:]
        current_dist = best_dist

        while time.time() - self.time < time_limit:
            # Get random neighbor
            new_route = self.get_random_neighbor(current_ans)

            # Calculate delta
            delta = self.get_distance(new_route) - current_dist

            # If delta is negative, update answer and distance.
            if delta < 0:
                current_ans = new_route[:]
                current_dist += delta
                best_ans = new_route[:]
                best_dist += delta

            # If delta is 0 or positive, accept with probability e^(-delta/temp).
            else:
                if math.exp(-delta / temp) >= random.random():
                    print(f'accepted {self.get_distance(new_route)}, current temperature is {temp}')
                    current_ans = new_route[:]
                    current_dist += delta

            # Update temperature.
            temp *= alpha

        self.ans = best_ans[:]
        self.best_dist = self.get_distance(self.ans)

    def print_solution(self):
        print(self.N)
        print(*self.ans)
        print(f'\nBest distance found: {self.best_dist}')
        print(f'Time taken: {time.time() - self.time}')


def main():
    # N, K, distance_matrix = import_data_input()
    N, K, distance_matrix = import_data_file('input100.txt')

    sol = Solver(N, K, distance_matrix)
    sol.solve_simulated_annealing(initial_temp=5000, alpha=0.99, time_limit=180)
    sol.print_solution()


if __name__ == "__main__":
    main()

