from parsing import parse_file
import sys

MAX_DEPTH = 999


# TODO: use max_delay
def dfs(stocks, processes, optimization):
    def helper(operations, current_cycles, depth):
        nonlocal best_cycles, best_operations
        if current_cycles >= best_cycles or depth >= MAX_DEPTH:
            return
        if optimization.stock_name in stocks:
            best_cycles = current_cycles
            best_operations = operations.copy()
            return

        for process_name, process in processes.items():
            if all(v <= stocks.get(k, 0) for k, v in process.inputs.items()):
                for k, v in process.inputs.items():
                    stocks[k] -= v
                for k, v in process.outputs.items():
                    stocks[k] += v
                operations.append(process_name)
                helper(operations, current_cycles + process.nb_cycles, depth + 1)
                operations.pop()
                for k, v in process.outputs.items():
                    stocks[k] -= v
                for k, v in process.inputs.items():
                    stocks[k] += v

    best_cycles = sys.maxsize
    best_operations = None
    helper([], 0, 0)
    return best_cycles, best_operations


def main():
    try:
        assert len(sys.argv) == 3
        max_delay = float(sys.argv[2])
    except (AssertionError, ValueError):
        print(f"Usage: python {sys.argv[0]} <filename> <max_delay>", file=sys.stderr)
        print(f"Example: python {sys.argv[0]} resources/steak 3.14", file=sys.stderr)
        sys.exit(1)
    stocks, processes, optimization = parse_file(sys.argv[1])
    print(dfs(stocks, processes, optimization))


if __name__ == "__main__":
    main()
