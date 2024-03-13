from copy import deepcopy
from heapq import heappop
from pprint import pprint
import random
import time
from parsing import parse_file
import sys

class Solution

def solver_dfs(stocks, processes, optimization, final_time):
    MAX_DEPTH = 999

    def helper(operations, current_cycles, depth):
        nonlocal best_cycles, best_operations, best_stocks, max_recursion_limit, timeout
        max_recursion_limit = depth >= MAX_DEPTH
        timeout = time.time() > final_time
        if current_cycles >= best_cycles or max_recursion_limit or timeout:
            return
        if stocks[optimization.stock_name] > 0:
            best_cycles = current_cycles
            best_operations = operations.copy()
            best_stocks = stocks.copy()
            return
        random.shuffle(processes)
        for process in processes:
            if all(v <= stocks.get(k, 0) for k, v in process.inputs.items()):
                for k, v in process.inputs.items():
                    stocks[k] -= v
                for k, v in process.outputs.items():
                    stocks[k] += v
                operations.append(process.name)
                helper(operations, current_cycles + process.nb_cycles, depth + 1)
                operations.pop()
                for k, v in process.outputs.items():
                    stocks[k] -= v
                for k, v in process.inputs.items():
                    stocks[k] += v

    best_cycles = sys.maxsize
    best_operations = None
    best_stocks = None
    max_recursion_limit = timeout = False
    helper([], 0, 0)
    return best_cycles, best_operations, best_stocks, max_recursion_limit, timeout


def solver_greedy(stocks, processes, optimization, final_time):
    MAX_OPERATIONS = 10**6
    heap = [(0, [], deepcopy(stocks))]
    best_cycles = sys.maxsize
    best_operations = None
    best_stocks = None
    max_recursion_limit = timeout = False
    for _ in range(MAX_OPERATIONS):
        current_cycles, current_operations, current_stocks = heappop(heap)

    return best_cycles, best_operations, best_stocks, max_recursion_limit, timeout


def main():
    try:
        assert len(sys.argv) == 3
        max_delay = float(sys.argv[2])  # TODO: use in each solving function
        assert max_delay > 0
        final_time = time.time() + max_delay
    except (AssertionError, ValueError):
        print(f"Usage: python {sys.argv[0]} <filename> <max_delay>", file=sys.stderr)
        print(f"Example: python {sys.argv[0]} resources/steak 3.14", file=sys.stderr)
        sys.exit(1)
    stocks, processes, optimization = parse_file(sys.argv[1])
    assert optimization.is_time, "for now"
    print(f"{sys.argv[1]} parsed succesfully")
    best_cycles, best_operations, best_stocks, max_recursion_limit, timeout = (
        solver_greedy(stocks, processes, optimization, final_time)
    )
    if best_operations is None:
        print(
            "Time limit exceeded"
            if timeout
            else "Max recursion limit"
            if max_recursion_limit
            else f"Impossible to create {optimization.stock_name}"
        )
    else:
        print(best_cycles, best_operations, best_stocks)


if __name__ == "__main__":
    main()
