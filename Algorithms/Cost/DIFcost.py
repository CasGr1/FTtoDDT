from FaultTree.FT import *
from Algorithms.Height.EDA import restrict
from Algorithms.Cost.CuDAcost import remove_cs, remove_var, find_likely_cut_set
# from Algorithms.Height.CuDA import remove_cs, remove_var, find_likely_cut_set
from Algorithms.Height.BUDA import expected_height


def DIDACOST(ft, cutsets):
    """
    This is an algorithm that transforms fault trees into diagnostic decision trees using cut sets
    :param ft: fault tree that will be converted
    :param cutsets: a set of all minimal cut sets
    :return: a diagnostic decision tree corresponding to ft
    """
    if not cutsets:
        return '0'
    if [] in cutsets:
        return '1'
    else:
        current_cs = find_likely_cut_set(ft, cutsets)
        var = sorted(current_cs, key=lambda var: ft.cost/(1-DIF(ft, var)))[0]
        return var, DIDACOST(ft, remove_cs(cutsets, var)), DIDACOST(ft, remove_var(cutsets, var))


def DIF(ft, var):
    subft = ft.find_vertex_by_name(var)
    prob = subft.prob
    return prob + (prob*(1-prob)*MIF(ft, var))/(ft.unreliability())


def MIF(ft, var):
    return restrict(ft, var, 1).unreliability() - restrict(ft, var, 0).unreliability()

if __name__ == "__main__":
    be1 = FT("BE1", FtElementType.BE, prob=0.1, cost=1)
    be2 = FT("BE2", FtElementType.BE, prob=0.3, cost=1)
    be3 = FT("BE3", FtElementType.BE, prob=0.2, cost=1)
    be4 = FT("BE4", FtElementType.BE, prob=0.15, cost=1)
    be5 = FT("BE5", FtElementType.BE, prob=0.05, cost=1)
    gate1 = FT("G1", FtElementType.AND, [be1, be2])
    gate3 = FT("G2", FtElementType.AND, [be4, be5])
    gate2 = FT("G3", FtElementType.OR, [be3, gate3])
    top = FT("TOP", FtElementType.OR, [gate1, gate2])

    ddt = DIDA(top, top.cut_set())
    print("DDT:", ddt)
    print("Exp Height:", expected_height(ddt, top.probabilities()))
    # print(MIF(top, "BE1"))
    # print(MIF(top, "BE2"))
    # print(MIF(top, "BE3"))
    # print(MIF(top, "BE4"))
    # print(MIF(top, "BE5"))
    # print(DIF(top, "BE1"))
    # print(DIF(top, "BE2"))
    # print(DIF(top, "BE3"))
    # print(DIF(top, "BE4"))
    # print(DIF(top, "BE5"))