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

    def find_vertex_by_name(self, name, ddt=None):
        if ddt is None:
            ddt = self
        if ddt.name == name:
            return ddt
        for child in ddt.children:
            result = self.find_vertex_by_name(name, child)
            if result is not None:
                return result
        return None

    def expected_cost_failure(self):
        expcost = 0
        failure_paths = [sublist for sublist in self.all_paths() if not sublist[-1].endswith('ZERO')]
        for path in failure_paths:
            cost = 0
            prob = 1
            path.pop()
            for elem in path:
                node = self.find_vertex_by_name(elem[0])
                cost += node.cost
                if elem[1] == 0:
                    prob *= (1-node.prob)
                elif elem[1] == 1:
                    prob *= node.prob
            expcost += prob*cost
        return expcost
        

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

    # def remove_duplicate_vertices(self, ddt=None, seen=None):
    #     if seen is None:
    #         seen = set()
    #     if ddt is None:
    #         ddt = self
    #     seen.add(ddt.name)
    #     if ddt.type == DdtElementType.DEC:
    #         if ddt.children[0].name in seen:
    #             ddt.children[0] = ddt.children[0].children[0].remove_duplicate_vertices(seen=seen)
    #         else:
    #             ddt.children[0] = ddt.children[0].remove_duplicate_vertices(seen=seen)
    #         if ddt.children[1].name in seen:
    #             ddt.children[1] = ddt.children[1].children[1].remove_duplicate_vertices(seen=seen)
    #         else:
    #             ddt.children[1] = ddt.children[1].remove_duplicate_vertices(seen=seen)
    #     return self

    def remove_duplicate_vertices(self, ddt=None, seen=None):
        """
        Remove duplicate vertices by name. When a child node has a name already seen,
        replace that child by its first child repeatedly until we find a node whose
        name is not seen (or no children remain), then continue recursion.
        Returns the (possibly replaced) node corresponding to `ddt`.
        """
        if seen is None:
            seen = set()
        if ddt is None:
            ddt = self

        # If this node's name was already seen, try to collapse it by
        # following its first-child chain until we find an unseen name (if possible),
        # then continue recursion from there.
        if ddt.name in seen:
            # find replacement by following first-child links
            replacement = ddt
            while getattr(replacement, "children", None) and replacement.name in seen:
                # choose the first child as replacement candidate
                first_children = replacement.children
                if not first_children:
                    break
                replacement = first_children[0]
            # if replacement is the same node (no collapse possible), just return it
            if replacement is ddt:
                return ddt
            # otherwise recursively clean the replacement and return it
            return replacement.remove_duplicate_vertices(ddt=replacement, seen=seen)

        # mark current node as seen
        seen.add(ddt.name)

        # process children generically (works for DEC or other node types)
        if getattr(ddt, "children", None):
            for i, child in enumerate(ddt.children):
                if child is None:
                    continue

                # collapse child while its name is in seen and it has at least one child to step into
                replacement = child
                while getattr(replacement, "children", None) and replacement.name in seen:
                    if not replacement.children:
                        break
                    replacement = replacement.children[0]

                # if replacement differs, or even if the same, recursively clean it (if not None)
                if replacement is not None:
                    ddt.children[i] = replacement.remove_duplicate_vertices(ddt=replacement, seen=seen)
                else:
                    ddt.children[i] = None

        return ddt

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
    be1 = FT("BE1", FtElementType.BE, prob=0.1, cost=10)
    be2 = FT("BE2", FtElementType.BE, prob=0.3, cost=10)
    be3 = FT("BE3", FtElementType.BE, prob=0.2, cost=10)
    be4 = FT("BE4", FtElementType.BE, prob=0.15, cost=10)
    be5 = FT("BE5", FtElementType.BE, prob=0.05, cost=10)
    gate1 = FT("G1", FtElementType.AND, [be1, be2])
    gate3 = FT("G2", FtElementType.AND, [be1, be5])
    gate2 = FT("G3", FtElementType.OR, [be3, gate3])
    top = FT("TOP", FtElementType.OR, [gate1, gate2])
    # edaddt, expcost = EDA(top, top.variables(), top.probabilities())
    from Algorithms.Cost.BUDAcost import *
    top.unreliability(add_unreliability=True)
    BUDAddt = BUDAcost(top)
    DDT = ddt_from_tuple(BUDAddt[0], top.probabilities(), top.cost_dict())

    # print(DDT.expected_cost_failure())
    DDT.print()
    DDT.remove_duplicate_vertices()
    DDT.print()
    # print(DDT.all_paths())

