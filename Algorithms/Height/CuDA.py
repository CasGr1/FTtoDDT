from FaultTree.FT import *


def CuDAprob(ft, cutsets):
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
        return var, CuDAprob(ft, remove_cs(cutsets, var)), CuDAprob(ft, remove_var(cutsets, var))


def CuDAsize(ft, cutsets):
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
        current_cs = sorted(cutsets, key=len)[0]
        var = find_min_var(ft, current_cs)
        return var, CuDAsize(ft, remove_cs(cutsets, var)), CuDAsize(ft, remove_var(cutsets, var))


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
        if current.prob < prob:
            prob = current.prob
            min_var = current.name
    return min_var


def find_likely_cut_set(ft, cutsets):
    """
    Function that calculates probability of all cut sets and returns the one with the highest probability
    :param ft: fault tree
    :param cutsets: set of cut sets
    :return: cut set in S with the highest probability
    """
    maxP = 0
    cutset = None
    for cs in cutsets:
        P = 1
        for vertex in cs:
            current = ft.find_vertex_by_name(vertex)
            P *= current.prob
        if P > maxP:
            maxP = P
            cutset = cs
    return cutset


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

    S = top.cut_set(top)
    print(CuDAprob(top, S))
    print(CuDAsize(top, S))
