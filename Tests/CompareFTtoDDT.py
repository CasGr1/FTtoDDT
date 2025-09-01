from DDT.DDT import *


def compare_ft_to_ddt(ddt, ft):
    cut_sets = ft.cut_set()
    all_paths = ddt.all_paths()


    for path in all_paths:
        result = path[-1]

        activated = {name for (name, val) in path [:-1] if isinstance((name, val), tuple) and val == 1}
        if result == 'ONE': violated = True
        if result == 'ZERO': violated = False

        if result == 'ONE':
            if not any(set(mcs).issubset(activated) for mcs in cut_sets):
                return False
        elif result == 'ZERO':
            if any(set(mcs).issubset(activated) for mcs in cut_sets):
                return False
    return True

if __name__ == "__main__":
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
    othertop = FT("TOP", FtElementType.AND, [gate1, gate2])
    edaddt, expcost = EDA(top, top.variables(), top.probabilities())
    DDT = ddt_from_tuple(edaddt, top.probabilities(), top.cost_dict())
    DDT.print()
    print(DDT.all_paths())
    print(compare_ft_to_ddt(top, DDT))
