import math
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Reaction:
    out_chem: str
    out_quant: int
    in_chems: Dict[str, int]

    @staticmethod
    def from_string(line: str) -> "Reaction":
        inputs, output = line.split(" => ")
        parse = lambda c: (int(c.split()[0]), c.split()[1])
        out_quant, out_chem = parse(output)
        in_chems = {chem: quant for quant, chem in map(parse, inputs.split(", "))}
        return Reaction(out_chem, out_quant, in_chems)


def topo_sort(reactions: Dict[str, Reaction]) -> List[str]:
    L = []
    S = {"ORE"}
    reactions = deepcopy(reactions)
    while S:
        n = S.pop()
        L.append(n)
        for k, reaction in reactions.items():
            if n in reaction.in_chems:
                del reaction.in_chems[n]
                if not reaction.in_chems:
                    S.add(k)
    if any(r.in_chems for r in reactions.values()):
        raise ValueError("Cycle found")
    return L


def a(reactions: Dict[str, Reaction], num_fuel: int = 1) -> int:
    order = reversed(topo_sort(reactions))
    to_create = defaultdict(int)
    to_create["FUEL"] = num_fuel
    for chem in order:
        if chem == "ORE":
            return to_create["ORE"]
        num_reactions = math.ceil(to_create[chem] / reactions[chem].out_quant)
        for in_chem, in_quant in reactions[chem].in_chems.items():
            to_create[in_chem] += in_quant * num_reactions


def b(reactions):
    lower, upper = 0, 1000000000
    one_trillion = 1_000_000_000_000
    prev = -1
    while True:
        middle = (lower + upper) // 2
        if middle == prev:
            return middle
        prev = middle
        ore_required = a(reactions, middle)
        if ore_required > one_trillion:
            upper = middle
        elif ore_required < one_trillion:
            lower = middle


def main():
    reactions = list(map(Reaction.from_string, open("input14.txt").read().splitlines()))
    reactions = {r.out_chem: r for r in reactions}
    print(b(reactions))


if __name__ == "__main__":
    main()
