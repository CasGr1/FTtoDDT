from FaultTree.FT import *


def CuDAtest(ft, cutsets):
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
        var = find_min_var(ft, current_cs)
        return var, CuDAtest(ft, remove_cs(cutsets, var)), CuDAtest(ft, remove_var(cutsets, var))


# def CuDAsize(ft, cutsets):
#     """
#     This is an algorithm that transforms fault trees into diagnostic decision trees using cut sets
#     :param ft: fault tree that will be converted
#     :param cutsets: a set of all minimal cut sets
#     :return: a diagnostic decision tree corresponding to ft
#     """
#     if not cutsets:
#         return '0'
#     if [] in cutsets:
#         return '1'
#     else:
#         current_cs = sorted(cutsets, key=len)[0]
#         var = find_min_var(ft, current_cs)
#         return var, CuDAsize(ft, remove_cs(cutsets, var)), CuDAsize(ft, remove_var(cutsets, var))


def remove_var(cutsets, remove):
    """
    This function removes all variables equal to remove argument in the set of all cut sets
    :param cutsets: set of cut sets
    :param remove: basic event that needs to be removed
    :return: set of cut sets where all basic events equal to remove are removed
    """
    updated_cutsets = [
        [e for e in cutset if e != remove]
        for cutset in cutsets
    ]
    return updated_cutsets


def remove_cs(cutsets, event):
    """
    This function removes all cut sets that contain the given event
    :param cutsets: set of cut sets
    :param event: event for which cut sets need to be removed
    :return: set of cut sets that do not contain event
    """
    updated_cutsets = [cutset for cutset in cutsets if event not in cutset]
    return updated_cutsets


def find_min_var(ft, current_cs):
    """
    Function to find the event with the highest probability within a cut set
    :param ft: fault tree that is being used
    :param current_cs: the cut set that is currently being used
    :return: variable with the highest failure probability
    """
    prob = float('inf')
    min_var = None
    for var in current_cs:
        current = ft.find_vertex_by_name(var)
        if current.cost < prob:
            prob = current.cost
            min_var = current.name
    return min_var


def find_likely_cut_set(ft, cutsets):
    """
    Function that calculates probability of all cut sets and returns the one with the highest probability
    :param ft: fault tree
    :param cutsets: set of cut sets
    :return: cut set in S with the highest probability
    """
    max = float('inf')

    cutset = None
    for cs in cutsets:
        P = 1
        C = 0
        for vertex in cs:
            current = ft.find_vertex_by_name(vertex)
            P *= current.prob
            C += current.cost
        comp = C
        if comp < max:
            max = comp
            cutset = cs
    return cutset



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
    be1 = FT("BE1", FtElementType.BE, prob=0.1, cost=1)
    be2 = FT("BE2", FtElementType.BE, prob=0.3, cost=1)
    be3 = FT("BE3", FtElementType.BE, prob=0.2, cost=1)
    be4 = FT("BE4", FtElementType.BE, prob=0.15, cost=1)
    be5 = FT("BE5", FtElementType.BE, prob=0.05, cost=1)
    gate1 = FT("G1", FtElementType.AND, [be1, be2])
    gate3 = FT("G2", FtElementType.AND, [be4, be5])
    gate2 = FT("G3", FtElementType.OR, [be3, gate3])
    top = FT("TOP", FtElementType.OR, [gate1, gate2])

    S = top.cut_set()
    p = CuDAprob(top, S)
    # s = CuDAsize(top, S)
    print("p:", p)
    print("exp_cost:", expected_cost(p, top.probabilities(top), top.cost_dict(top)))
    print('exp_height:', expected_height(p, top.probabilities(top)))

