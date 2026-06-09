from ortools.linear_solver import pywraplp

from discrete_optimization.cutting_stock_mip_all import CuttingStockMip


class CuttingStockColGen:
    def __init__(self, sizes, demands, wood_length):
        self.demands = demands
        self.sizes = sizes
        self.wood_length = wood_length
        self.n_sizes = len(sizes)

    def master(self, patterns=None):
        if not patterns:
            patterns = self._initialize_patterns()
        n_patterns = len(patterns)
        solver = pywraplp.Solver.CreateSolver("GLOP")
        q_pattern = self._create_vars_q_of_patterns(solver, patterns)

        constraints = {}
        constraints = constraints | self._satisfy_demand_constraint(solver, patterns, q_pattern)

        obj = solver.Objective()
        for p in range(n_patterns):
            obj.SetCoefficient(q_pattern[p], 1)
        obj.SetMinimization()

        solver.Solve()

        duals = [constraints[ct].dual_value() for ct in constraints]
        return solver, patterns, q_pattern, duals

    def _initialize_patterns(self):
        patterns = []
        for i, s in enumerate(self.sizes):
            pattern = [0] * self.n_sizes
            pattern[i] = self.wood_length // s
            patterns.append(pattern)
        return patterns

    def _create_vars_q_of_patterns(self, solver, patterns):
        q_pattern = []
        for p in range(len(patterns)):
            q_pattern.append(solver.NumVar(0, solver.infinity(), f"x_{p}"))
        return q_pattern

    def _satisfy_demand_constraint(self, solver, patterns, q_pattern):
        constraints = {}
        for s in range(self.n_sizes):
            constraints[s] = solver.Add(
                sum(patterns[p][s] * q_pattern[p] for p in range(len(patterns))) >= self.demands[s]
            )
        return constraints

    def pricing(self, duals):
        """
        Generates a new cutting pattern with negative reduced cost.
        """
        solver = pywraplp.Solver.CreateSolver("SCIP")
        item_count_in_pattern = self._create_vars_size_count_in_pattern(solver)

        self._capacity_constraint(solver, item_count_in_pattern)

        obj = sum(duals[i] * item_count_in_pattern[i] for i in range(self.n_sizes))
        solver.Maximize(obj)
        status = solver.Solve()

        if status != pywraplp.Solver.OPTIMAL:
            return None, 0

        new_pattern = [int(item_count_in_pattern[i].solution_value()) for i in range(self.n_sizes)]

        pattern_value = sum(duals[s] * new_pattern[s] for s in range(self.n_sizes))
        reduced_cost = 1 - pattern_value

        return new_pattern, reduced_cost

    def _create_vars_size_count_in_pattern(self, solver):
        """
        Decision: how many items of each size in pattern

        """
        size_count_in_pattern = []
        for i in range(self.n_sizes):
            ub = self.wood_length // self.sizes[i]
            size_count_in_pattern.append(solver.IntVar(0, ub, f"size_count_{i}"))
        return size_count_in_pattern

    def _capacity_constraint(self, solver, item_count_in_pattern):
        solver.Add(
            sum(self.sizes[s] * item_count_in_pattern[s] for s in range(self.n_sizes))
            <= self.wood_length
        )

    def solve(self, MAX_ITER=100, patterns=None):
        for i in range(MAX_ITER):
            solver, patterns, q_pattern, duals = self.master(patterns=patterns)
            print(f"\n Best objective iteration = {i}: {solver.Objective().Value()}")
            print(f"demands = {self.demands}")
            print([(p, q_pattern[i].solution_value()) for i, p in enumerate(patterns)])

            print(f"sizes={self.sizes}")
            new_pattern, reduced_cost = self.pricing(duals)
            print(f"new_pattern = {new_pattern}, reduced_cost = {reduced_cost}")

            if reduced_cost < -1e-6:
                patterns.append(new_pattern)
            else:
                print("Optimal LP reached.")
                break

        # solve with chosen patterns,
        # TODO replace for branching (branch and price)
        print("\n\nSolve MIP with chosen patterns")
        cm = CuttingStockMip(self.sizes, self.demands, self.wood_length)
        sol, objective = cm.solve(patterns)
        return sol, objective
