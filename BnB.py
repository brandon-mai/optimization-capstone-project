import time


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
        self.best_dist = float('inf')
        self.time = time.time()

        self.current_node = 0
        self.capacity = 0

    def solve_backtrack(self, curr_route=(), curr_dist=0):
        curr_route = [node for node in curr_route]

        for next_node in range(1, self.Num_Nodes):

            if self.visited[next_node] or self.capacity + self.demands[next_node] > self.K:
                continue

            if next_node > self.N and not self.visited[next_node - self.N]:
                continue

            curr_route.append(next_node)
            curr_dist += self.Distance_Matrix[self.current_node][next_node]
            self.visited[next_node] = True
            self.capacity += self.demands[next_node]

            if len(curr_route) == self.Num_Nodes - 1:
                total_dist = curr_dist + self.Distance_Matrix[self.current_node][0]
                if total_dist < self.best_dist:
                    self.best_dist = total_dist
                    self.ans = [node for node in curr_route]
            else:
                last_node = self.current_node
                self.current_node = next_node
                self.solve_backtrack(tuple(curr_route), curr_dist)
                self.current_node = last_node

            curr_route.remove(next_node)
            curr_dist -= self.Distance_Matrix[self.current_node][next_node]
            self.visited[next_node] = False
            self.capacity -= self.demands[next_node]

    def solve_bnb(self, curr_route=(), curr_dist=0):
        curr_route = [node for node in curr_route]

        # Find the smallest edge to unvisited nodes for BnB
        unvisited_nodes = [tup[0] for tup in list(enumerate(self.visited)) if tup[1] is False]
        reduced_mat = [[self.Distance_Matrix[row][node] for node in unvisited_nodes] for row in unvisited_nodes]
        reduced_mat = [reduced_mat[row][:row] + reduced_mat[row][row+1:] for row in range(len(unvisited_nodes))]
        smallest_edge = min([min(row) for row in reduced_mat])

        for next_node in range(1, self.Num_Nodes):

            if self.visited[next_node] or self.capacity + self.demands[next_node] > self.K:
                continue

            if next_node > self.N and not self.visited[next_node - self.N]:
                continue

            curr_route.append(next_node)
            curr_dist += self.Distance_Matrix[self.current_node][next_node]
            self.visited[next_node] = True
            self.capacity += self.demands[next_node]

            if len(curr_route) == self.Num_Nodes - 1:
                total_dist = curr_dist + self.Distance_Matrix[self.current_node][0]
                if total_dist < self.best_dist:
                    self.best_dist = total_dist
                    self.ans = [node for node in curr_route]
            else:
                if curr_dist + (self.Num_Nodes - 1 - len(curr_route)) * smallest_edge < self.best_dist:
                    last_node = self.current_node
                    self.current_node = next_node
                    self.solve_bnb(tuple(curr_route), curr_dist)
                    self.current_node = last_node

            curr_route.remove(next_node)
            curr_dist -= self.Distance_Matrix[self.current_node][next_node]
            self.visited[next_node] = False
            self.capacity -= self.demands[next_node]

    def print_solution(self):
        print(self.N)
        print(*self.ans)
        print(f'\nBest distance found: {self.best_dist}')
        print(f'Time taken: {time.time() - self.time}')


def main():
    # N, K, distance_matrix = import_data_input()
    N, K, distance_matrix = import_data_file('input5.txt')

    sol = Solver(N, K, distance_matrix)
    sol.solve_bnb()
    sol.print_solution()


if __name__ == "__main__":
    main()
