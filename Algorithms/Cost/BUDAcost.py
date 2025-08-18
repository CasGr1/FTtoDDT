from FaultTree.FT import *


def BUDAcost(ft):
    """
    This is an algorithm for transforming fault trees to diagnostic decision trees using a bottom-up approach
    :param ft: the fault tree that needs to be performed
    :return: diagnostic decision tree
    """
    if ft.type == FtElementType.BE:
        return ft.name, '0', '1'
    if ft.type == FtElementType.AND:
        ordered_children = sorted(ft.children, key=lambda child: child.prob * child.cost, reverse=True)
        result = None
        for child in ordered_children:
            if result is None:
                result = BUDAcost(child)
            else:
                result = replace(result, '1', BUDAcost(child))
        return result
    if ft.type == FtElementType.OR:
        ordered_children = sorted(ft.children, key=lambda child: child.prob * child.cost)
        result = None
        for child in ordered_children:
            if result is None:
                result = BUDAcost(child)
            else:
                result = replace(result, '0', BUDAcost(child))
        return result


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


def expected_cost(ddt, P, cost, acc_cost=0):
    """
    Function that calculates the expected height of a diagnostic decision tree
    :param ddt: the decision tree that is used
    :param P: the probabilities of basic events in the decision tree
    :param cost: used for recursive step
    :return: the expected height of ddt
    """
    node, low, high = ddt
    p_high = P[node]
    p_low = 1 - p_high
    acc_cost += cost[node]

    if low in ('0', '1'):
        low_exp = acc_cost
    else:
        low_exp = expected_cost(low, P, cost, acc_cost)
    if high in ('0', '1'):
        high_exp = acc_cost
    else:
        high_exp = expected_cost(high, P, cost, acc_cost)
    return p_low * low_exp + p_high * high_exp


if __name__ == "__main__":
    be1 = FT("BE1", FtElementType.BE, prob=0.1, cost=10)
    be2 = FT("BE2", FtElementType.BE, prob=0.3, cost=1)
    be3 = FT("BE3", FtElementType.BE, prob=0.2, cost=1)
    be4 = FT("BE4", FtElementType.BE, prob=0.15, cost=1)
    be5 = FT("BE5", FtElementType.BE, prob=0.05, cost=1)
    gate1 = FT("G1", FtElementType.AND, [be1, be2])
    gate3 = FT("G2", FtElementType.AND, [be4, be5])
    gate2 = FT("G3", FtElementType.OR, [be3, gate3])
    top = FT("TOP", FtElementType.OR, [gate1, gate2])
    top.unreliability(add_unreliability=True)
    DDT = BUDAcost(top)
    print(DDT)
    print(expected_cost(DDT, top.probabilities(top), top.cost_dict(top)))