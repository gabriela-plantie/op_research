from itertools import product

from ortools.linear_solver import pywraplp


def initialize_patterns(sizes, wood_length):
    patterns = []
    max_counts = [wood_length // s for s in sizes]

    patterns = []

    for pattern in product(*[range(m + 1) for m in max_counts]):
        if sum(c * s for c, s in zip(pattern, sizes, strict=False)) <= wood_length:
            patterns.append(pattern)
    return patterns


class CuttingStockMip:
    def __init__(self, sizes, demands, wood_length):
        self.demands = demands
        self.sizes = sizes
        self.wood_length = wood_length
        self.n_sizes = len(sizes)

    def solve(self, patterns):
        solver = pywraplp.Solver.CreateSolver("CBC")

        wood = [
            solver.IntVar(0, sum(self.demands) * max(self.sizes), f"wood_{p}")
            for p in range(len(patterns))
        ]

        # Demand constraints
        for i in range(len(self.sizes)):
            solver.Add(
                sum(patterns[p][i] * wood[p] for p in range(len(patterns))) >= self.demands[i]
            )

        # Minimize number of stock rolls
        solver.Minimize(sum(wood))

        solver.Solve()

        solution = []
        for p in range(len(patterns)):
            solution.append((patterns[p], int(wood[p].solution_value())))
        objective = solver.Objective().Value()
        print(f"\n Objective = {i}: {objective}")
        return solution, objective
