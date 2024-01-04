import time

# GREEDY ALGORITHM THAT CHOOSES THE NEAREST ADJACENT NODE EVERY TIME


def import_data_input():
    N, K = map(int, input().split())
    distance_matrix = []
    for i in range(2 * N + 1):
        distance_matrix.append(list(map(int, input().split())))
    return N, K, distance_matrix


def import_data_file(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    N, K = [int(num) for num in lines[0].rstrip().split()]
    distance_matrix = [[int(num) for num in row.rstrip().split()] for row in lines[1:]]
    f.close()
    return N, K, distance_matrix


class Solver:
    def __init__(self, N, K, distance_matrix):
        self.N = N
        self.K = K
        self.Num_Nodes = 2 * N + 1
        self.Distance_Matrix = distance_matrix

        self.visited = [False for _ in range(self.Num_Nodes)]
        self.demands = [1 if 1 <= i <= N else -1 for i in range(self.Num_Nodes)]
        self.ans = list()
        self.best_dist = 0
        self.time = time.time()

        self.current_node = 0
        self.capacity = 0

    def solve_greedy(self):
        for _ in range(self.Num_Nodes - 1):
            min_dist = float('inf')
            best_node = -1

            for node in range(1, self.Num_Nodes):
                if self.visited[node] or self.capacity + self.demands[node] > self.K:
                    continue

                if node > self.N and not self.visited[node - self.N]:
                    continue

                if self.Distance_Matrix[self.current_node][node] < min_dist:
                    min_dist = self.Distance_Matrix[self.current_node][node]
                    best_node = node

            self.ans.append(best_node)
            self.visited[best_node] = True
            self.capacity += self.demands[best_node]
            self.best_dist += self.Distance_Matrix[self.current_node][best_node]

            self.current_node = best_node

        self.best_dist += self.Distance_Matrix[self.current_node][0]

    def print_solution(self):
        print(self.N)
        print(*self.ans)
        print(f'\nBest distance found: {self.best_dist}')
        print(f'Time taken: {time.time() - self.time}')


def main():
    # N, K, distance_matrix = import_data_input()
    N, K, distance_matrix = import_data_file('input100.txt')

    sol = Solver(N, K, distance_matrix)
    sol.solve_greedy()
    sol.print_solution()


if __name__ == "__main__":
    main()
