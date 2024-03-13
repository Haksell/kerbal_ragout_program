from pprint import pprint
import random
from parsing import parse_file
import sys

MAX_DEPTH = 999


def dfs(stocks, processes, optimization):
    def helper(operations, current_cycles, depth):
        nonlocal best_cycles, best_operations, best_stocks
        if current_cycles >= best_cycles or depth >= MAX_DEPTH:
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
    helper([], 0, 0)
    return best_cycles, best_operations, best_stocks


def main():
    try:
        assert len(sys.argv) == 3
        max_delay = float(sys.argv[2])  # TODO: use in each solving function
    except (AssertionError, ValueError):
        print(f"Usage: python {sys.argv[0]} <filename> <max_delay>", file=sys.stderr)
        print(f"Example: python {sys.argv[0]} resources/steak 3.14", file=sys.stderr)
        sys.exit(1)
    stocks, processes, optimization = parse_file(sys.argv[1])
    print(f"{sys.argv[1]} parsed succesfully")
    pprint(stocks)
    print(dfs(stocks, processes, optimization))


if __name__ == "__main__":
    main()
