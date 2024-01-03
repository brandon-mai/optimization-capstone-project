import time
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


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

        self.distance_matrix = distance_matrix
        self.visited = [False for _ in range(self.Num_Nodes)]
        self.demands = [1 if 1 <= i <= N else -1 for i in range(self.Num_Nodes)]
        self.ans = list()
        self.best_dist = float('inf')
        self.time = time.time()

        self.current_node = 0
        self.capacity = 0

    def solve_cp(self):
        pickups_deliveries = [(i, i + self.N) for i in range(1, self.N + 1)]
        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(self.distance_matrix), 1, 0)

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        # Define cost of each arc.
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)  # takes 2 arguments
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Distance constraint.
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            1000,  # vehicle maximum travel distance
            True,  # start cumul to zero
            "Distance",
        )
        distance_dimension = routing.GetDimensionOrDie("Distance")

        # Define Transportation Requests.
        for request in pickups_deliveries:
            pickup_index = manager.NodeToIndex(request[0])
            delivery_index = manager.NodeToIndex(request[1])
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            # passenger must be picked up and dropped off by the same vehicle
            routing.solver().Add(
                routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index)
            )
            # passenger must be picked up before dropped off
            routing.solver().Add(
                distance_dimension.CumulVar(pickup_index) <= distance_dimension.CumulVar(delivery_index)
            )

        # Add Capacity constraint.
        def demand_callback(from_index):
            """Returns the demand of the node."""
            from_node = manager.IndexToNode(from_index)
            return 1 if from_node <= self.N else -1

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)  # unary: takes 1 argument
        routing.AddDimension(
            demand_callback_index,
            0,  # null capacity slack
            self.K,  # vehicle maximum capacities
            True,  # start cumul to zero
            "Capacity",
        )

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
        # search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING
        # search_parameters.time_limit.seconds = 10
        # search_parameters.log_search = True

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Add solution to Solver object's property.
        if solution:
            index = routing.Start(0)
            self.ans = [manager.IndexToNode(index)]
            while not routing.IsEnd(index):
                index = solution.Value(routing.NextVar(index))
                self.ans.append(manager.IndexToNode(index))
            self.ans = self.ans[1:-1]
            self.best_dist = solution.ObjectiveValue()

    def print_solution(self):
        print(self.N)
        print(*self.ans)
        print(f'\nBest distance found: {self.best_dist}')
        print(f'Time taken: {time.time() - self.time}')


def main():
    # N, K, distance_matrix = import_data_input()
    N, K, distance_matrix = import_data_file('input10.txt')

    sol = Solver(N, K, distance_matrix)
    sol.solve_cp()
    sol.print_solution()


if __name__ == "__main__":
    main()
