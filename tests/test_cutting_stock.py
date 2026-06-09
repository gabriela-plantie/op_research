import pytest

from discrete_optimization.branch_and_price import BranchAndPrice
from discrete_optimization.cutting_stock_col_gen import CuttingStockColGen
from discrete_optimization.cutting_stock_mip_all import CuttingStockMip, initialize_patterns


@pytest.mark.parametrize(
    "sizes, wood_length, expected",
    [
        (
            [2, 3],
            5,
            {(2, 0), (1, 1)},
        ),
        (
            [1],
            3,
            {(3,)},
        ),
        (
            [2, 5],
            10,
            {
                (5, 0),
                (0, 2),
                (2, 1),
            },
        ),
    ],
)
def test_generate_patterns(sizes, wood_length, expected):
    patterns = set(initialize_patterns(sizes, wood_length))
    assert expected.issubset(patterns)


@pytest.mark.parametrize(
    "sizes, wood_length, demands, expected",
    [
        ([2, 3, 5, 7], 10, [61, 40, 32, 100], 117),
    ],
)
def test_solve_mip_all(sizes, wood_length, demands, expected):
    patterns = initialize_patterns(sizes, wood_length)
    cm = CuttingStockMip(sizes, demands, wood_length)
    sol, objective = cm.solve(patterns)
    assert objective == expected


@pytest.mark.parametrize(
    "sizes, wood_length, demands, expected",
    [
        ([2, 3, 5, 7], 10, [61, 40, 32, 100], 117),
    ],
)
def test_solve_col_gen(sizes, wood_length, demands, expected):
    cg = CuttingStockColGen(sizes, demands, wood_length)
    sol, objective = cg.solve()
    assert objective == expected


@pytest.mark.parametrize(
    "sizes, wood_length, demands, expected",
    [
        ([2, 3, 5, 7], 10, [61, 40, 32, 100], 117),
    ],
)
def test_solve_branch_and_price(sizes, wood_length, demands, expected):
    bp = BranchAndPrice(demands, sizes, wood_length)
    best_solution, best_obj = bp.solve()

    print("Best objective:", best_obj)
    print("Solution:", best_solution)
    assert best_obj == expected
