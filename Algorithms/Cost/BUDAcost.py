from FaultTree.FT import *
from FaultTree.FTParser import *
from DDT.DDT import *

def BUDAcost(ft):
    """
    This is an algorithm for transforming fault trees to diagnostic decision trees using a bottom-up approach
    :param ft: the fault tree that needs to be performed
    :return: diagnostic decision tree
    """
    if ft.type == FtElementType.BE:
        return (ft.name, '0', '1'), ft.prob, ft.cost

    subtrees  = [BUDAcost(ch) for ch in ft.children]
    if ft.type == FtElementType.AND:
        ordered_children = sorted(subtrees, key=lambda x: x[2]/(1-x[1]))
        ft.cost = expected_cost_subft(ordered_children, 'AND')
        result = None
        for child, _, _ in ordered_children:
            if result is None:
                result = child
            else:
                result = replace(result, '1', child)
        return result, ft.prob, ft.cost

    if ft.type == FtElementType.OR:
        ordered_children = sorted(subtrees, key=lambda x: x[2]/(1-x[1]), reverse=True)
        ft.cost = expected_cost_subft(ordered_children, 'OR')
        result = None
        for child, _, _ in ordered_children:
            if result is None:
                result = child
            else:
                result = replace(result, '0', child)
        return result, ft.prob, ft.cost


def replace(struct, original, replacement):
    """
    Replaces all items that are equal to original with replacement
    :param struct: the tuple that is used
    :param original: the item that needs to be replaced
    :param replacement: what original is replaced with
    :return: struct with original replaced by replacement
    """
    if isinstance(struct, tuple):
        return tuple(replace(item, original, replacement) for item in struct)
    elif struct == original:
        return replacement
    else:
        return struct


def expected_cost_subft(ordered_children, gate_type):
    expected = 0.0
    if gate_type == 'OR':
        prob_prefix = 1.0
        for _, prob, cost in ordered_children:
            expected += prob_prefix * cost
            prob_prefix *= (1 - prob)
    elif gate_type == 'AND':
        prob_prefix = 1.0
        for _, prob, cost in ordered_children:
            expected += prob_prefix * cost
            prob_prefix *= prob
    return expected


if __name__ == "__main__":
#     be1 = FT("BE1", FtElementType.BE, prob=0.1, cost=10)
#     be2 = FT("BE2", FtElementType.BE, prob=0.3, cost=1)
#     be3 = FT("BE3", FtElementType.BE, prob=0.2, cost=1)
#     be4 = FT("BE4", FtElementType.BE, prob=0.15, cost=1)
#     be5 = FT("BE5", FtElementType.BE, prob=0.05, cost=1)
#     gate1 = FT("G1", FtElementType.AND, [be1, be2], cost=0)
#     gate3 = FT("G2", FtElementType.AND, [be4, be5], cost=0)
#     gate2 = FT("G3", FtElementType.OR, [be3, gate3], cost=0)
#     top = FT("TOP", FtElementType.OR, [gate1, gate2], cost=0)
    top = FTParse("FaultTree/FTexamples/Cost/test.dft")
    top.unreliability(add_unreliability=True)
    DDT = BUDAcost(top)
    convertedDDT = ddt_from_tuple(DDT[0], top.probabilities(), top.cost_dict())
    convertedDDT.print()
    print(convertedDDT.expected_cost())
