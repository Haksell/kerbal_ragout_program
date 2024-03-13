from collections import defaultdict
from dataclasses import dataclass
import re
import sys
from typing import List, Dict

# TODO: unknown stock for process or optimization

REGEX_STOCK = r"(\w+):(\d+)"
REGEX_DICT = r"(\((?:\w+):(?:\d+)(?:;(?:\w+):(?:\d+))*\))"


@dataclass
class Process:
    name: str
    inputs: List[Dict[str, int]]
    outputs: List[Dict[str, int]]
    nb_cycles: int


@dataclass
class Optimization:
    stock_name: str
    is_time: bool


def __parse_process_dict(s):
    s = s[1:-1]
    res = dict()
    for pair in s.split(";"):
        k, v = pair.split(":")
        res[k] = int(v)
    return res


def parse_file(filename):
    stocks = defaultdict(int)
    processes = []
    optimization = None
    for line in open(filename):
        if line.startswith("#"):
            continue
        line = line.strip()
        stock_match = re.fullmatch(REGEX_STOCK, line)
        if stock_match:
            name, quantity = stock_match.groups()
            if name in stocks:
                print("DOUBLON STOCK", file=sys.stderr)
                sys.exit(1)
            stocks[name] = int(quantity)
            continue
        process_match = re.fullmatch(rf"(\w+):{REGEX_DICT}:{REGEX_DICT}:(\d+)", line)
        if process_match:
            name, inputs, outputs, nb_cycles = process_match.groups()
            if any(p.name == name for p in processes):
                print("DOUBLON PROCESS", file=sys.stderr)
                sys.exit(1)
            processes.append(
                Process(
                    name,
                    __parse_process_dict(inputs),
                    __parse_process_dict(outputs),
                    int(nb_cycles),
                )
            )
            continue
        optimize_match = re.fullmatch(r"optimize:\((time;)?(\w+)\)", line)
        if optimize_match:
            if optimization is not None:
                print("DOUBLON OPTIMIZATION", file=sys.stderr)
                sys.exit(1)
            is_time, stock_name = optimize_match.groups()
            optimization = Optimization(stock_name, is_time is not None)
            continue
        print(f"Failed to parse line: {line}", file=sys.stderr)
        sys.exit(1)
    return stocks, processes, optimization
