from enum import Enum

class DdtElementType(Enum):
    DEC = 1
    ONE = 2
    ZERO = 3


class DDT:
    def __init__(self, name, DdtElement, children=None, prob=None, cost=None):
        if children is None:
            children = []
        self.name = name
        self.type = DdtElement
        self.children = children
        self.prob = prob
        self.cost = cost

    def expected_height(self, ddt=None, depth=0):
        if ddt is None:
            ddt = self
        if ddt.type is not DdtElementType.DEC:
            return depth
        left = (1 - ddt.prob) * self.expected_height(ddt.children[0], depth + 1)
        right = ddt.prob * self.expected_height(ddt.children[1], depth + 1)
        return left + right

    def expected_cost(self, ddt=None):
        if ddt is None:
            ddt = self
        if ddt.type != DdtElementType.DEC:
            return 0 # leaf cost
        left = (1 - ddt.prob) * self.expected_cost(ddt.children[0])
        right = ddt.prob * self.expected_cost(ddt.children[1])
        return ddt.cost + left + right

    def all_paths(self, path=None):
        if path is None:
            path = []

        if self.type == DdtElementType.DEC:
            paths = []
            left_paths = self.children[0].all_paths(path + [(self.name, 0)])
            right_paths = self.children[1].all_paths(path + [(self.name, 1)])
            paths.extend(left_paths)
            paths.extend(right_paths)
            return paths
        else:
            # Leaf node: return path + result
            return [path + [f"{self.type.name}"]]

    def print(self):
        print(self.to_string())

    def to_string(self, level=0):
        indent = "  " * level
        if self.cost is not None:
            result = f"{indent}- {self.name} (type: {self.type}, prob: {self.prob}, cost: {self.cost})\n"
        elif self.prob is not None:
            result = f"{indent}- {self.name} (type: {self.type}, prob: {self.prob})\n"
        else:
            result = f"{indent}- {self.name} (type: {self.type})\n"
        for child in self.children:
            result += child.to_string(level + 1)
        return result

def ddt_from_tuple(ddt, prob=None, cost=None):
    if isinstance(ddt, tuple):
        if cost is not None:
            p= prob[ddt[0]]
            c = cost[ddt[0]]
            return DDT(ddt[0], DdtElementType.DEC, children=[ddt_from_tuple(ddt[1], prob, cost), ddt_from_tuple(ddt[2], prob, cost)], prob=p, cost=c)
        elif prob is not None:
            p = prob[ddt[0]]
            return DDT(ddt[0], DdtElementType.DEC, children=[ddt_from_tuple(ddt[1], prob), ddt_from_tuple(ddt[2], prob)], prob=p)
        return DDT(ddt[0], DdtElementType.DEC, children=[ddt_from_tuple(ddt[1], prob), ddt_from_tuple(ddt[2], prob)])
    elif ddt == '0':
        return DDT('ZERO', DdtElementType.ZERO)
    elif ddt == '1':
        return DDT('ONE', DdtElementType.ONE)

if __name__ == "__main__":
    # ddtexample = ('BE3', ('BE1', ('BE5', '0', ('BE4', '0', '1')), ('BE2', ('BE5', '0', ('BE4', '0', '1')), '1')), '1')
    # dec = ddt_from_tuple(ddtexample)
    # dec.print()

    from FaultTree.FT import *
    from Algorithms.Height.EDA import *
    be1 = FT("BE1", FtElementType.BE, prob=0.1, cost=1)
    be2 = FT("BE2", FtElementType.BE, prob=0.3, cost=1)
    be3 = FT("BE3", FtElementType.BE, prob=0.2, cost=1)
    be4 = FT("BE4", FtElementType.BE, prob=0.15, cost=1)
    be5 = FT("BE5", FtElementType.BE, prob=0.05, cost=1)
    gate1 = FT("G1", FtElementType.AND, [be1, be2])
    gate3 = FT("G2", FtElementType.AND, [be4, be5])
    gate2 = FT("G3", FtElementType.OR, [be3, gate3])
    top = FT("TOP", FtElementType.OR, [gate1, gate2])
    edaddt, expcost = EDA(gate1, gate1.variables(), gate1.probabilities())
    DDT = ddt_from_tuple(edaddt, gate1.probabilities(), gate1.cost_dict())
    # DDT.print()
    print(DDT.all_paths())
    print(DDT.expected_height())
    print(DDT.expected_cost())

