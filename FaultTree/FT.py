from enum import Enum
from itertools import product
class FtElementType(Enum):
    BE = 1
    AND = 2
    OR = 3

class FT:
    def __init__(self, name, ftelement, children=None, prob=0, cost=0):
        if children == None:
            children = []
        self.name = name
        self.type = ftelement
        self.children = children
        self.prob = prob
        self.cost = cost

    def variables(self, ft=None):
        if ft is None:
            ft = self

        if ft.type == FtElementType.BE:
            return {ft.name}

        variables = set()
        for child in ft.children:
            variables.update(self.variables(child))
        return variables

    def vertices(self, ft=None):
        if ft is None:
            ft = self

        if ft.type == FtElementType.BE:
            return {ft.name}

        variables = {ft.name}
        for child in ft.children:
            variables.update(self.vertices(child))
        return variables

    def probabilities(self, ft=None):
        if ft is None:
            ft = self

        if ft.type == FtElementType.BE:
            return {ft.name: ft.prob}

        events = {}
        for child in ft.children:
            events.update(self.probabilities(child))
        return events

    def cost_dict(self, ft=None):
        if ft is None:
            ft = self

        if ft.type == FtElementType.BE:
            return {ft.name: ft.cost}

        events = {}
        for child in ft.children:
            events.update(self.cost_dict(child))
        return events

    def cut_set(self, ft=None):
        if ft is None:
            ft = self

        if ft.type == FtElementType.BE:
            return [[ft.name]]

        if ft.type == FtElementType.AND:
            child_cut_sets = [self.cut_set(child) for child in ft.children]
            result = []

            for combination in product(*child_cut_sets):
                merged = []
                for cut in combination:
                    merged.extend(cut)
                result.append(sorted(set(merged)))
            return result

        if ft.type == FtElementType.OR:
            result = []
            for child in ft.children:
                new = self.cut_set(child)
                result += new
            return result

    def path_set(self, ft=None):
        if ft is None:
            ft = self

        if ft.type == FtElementType.BE:
            return [[ft.name]]

        if ft.type == FtElementType.OR:
            child_cut_sets = [self.path_set(child) for child in ft.children]
            result = []

            for combination in product(*child_cut_sets):
                merged = []
                for cut in combination:
                    merged.extend(cut)
                result.append(sorted(set(merged)))
            return result

        if ft.type == FtElementType.AND:
            result = []
            for child in ft.children:
                new = self.path_set(child)
                result += new
            return result

    def unreliability(self, ft=None, add_unreliability=False):
        if ft is None:
            ft = self

        if ft.type == FtElementType.BE:
            return ft.prob

        if ft.type == FtElementType.AND:
            result = 1
            for child in ft.children:
                result *= self.unreliability(child, add_unreliability)
            if add_unreliability:
                ft.prob = result
            return result

        if ft.type == FtElementType.OR:
            result = 1
            for child in ft.children:
                result *= (1 - self.unreliability(child, add_unreliability))
            if add_unreliability:
                ft.prob = result
            return 1 - result

    def find_vertex_by_name(self, name, ft=None):
        if ft is None:
            ft = self
        if ft.name == name:
            return ft
        for child in ft.children:
            result = self.find_vertex_by_name(name, child)
            if result is not None:
                return result
        return None
    def print(self, indent=0):
        print(" "*indent + f"{self.name} prob: {self.prob} (", end="")
        if self.type == FtElementType.BE:
            print("BE)")
        elif self.type == FtElementType.AND:
            print("AND)")
        elif self.type == FtElementType.OR:
            print("OR)")

        for child in self.children:
            child.print(indent+1)


if __name__ == "__main__":
    be1 = FT("BE1", FtElementType.BE, prob=0.1)
    be2 = FT("BE2", FtElementType.BE, prob=0.3)
    be3 = FT("BE3", FtElementType.BE, prob=0.2)
    be4 = FT("BE4", FtElementType.BE, prob=0.15)
    be5 = FT("BE5", FtElementType.BE, prob=0.05)
    gate1 = FT("G1", FtElementType.AND, [be1, be2])
    gate3 = FT("G2", FtElementType.AND, [be4, be5])
    gate2 = FT("G3", FtElementType.OR, [be3, gate3])
    top = FT("TOP", FtElementType.OR, [gate1, gate2])
    # current = top.find_vertex_by_name(top, "G3")
    # print(current.name)
    # print(top.variables(top))
    # print(top.probabilities(top))
    # print(top.cut_set(top))
    # print(top.path_set(top))
    # print(top.unreliability(top))
    print(top.cost_dict(top))


