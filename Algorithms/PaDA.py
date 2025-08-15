from FaultTree.FT import *
from Algorithms.CuDA import remove_cs, remove_var

def PaDAprob(ft, S):
    """
    This is an algorithm that transforms fault trees into diagnostic decision trees using path sets
    It picks the path sets based on probability
    :param ft: fault tree that will be converted
    :param S: a set of all minimal cut sets
    :return: a diagnostic decision tree corresponding to ft
    """

    if not S:
        return '0'
    if [] in S:
        return '1'
    else:
        current_cs = find_min_path_set(ft, S)
        var = find_max_var(ft, current_cs)
        return var, PaDAprob(ft, remove_cs(S, var)), PaDAprob(ft, remove_var(S, var))


def PaDAsize(ft, S):
    """
    This is an algorithm that transforms fault trees into diagnostic decision trees using path sets
    It picks path sets based on size
    :param ft: fault tree that will be converted
    :param S: a set of all minimal cut sets
    :return: a diagnostic decision tree corresponding to ft
    """

    if not S:
        return '0'
    if [] in S:
        return '1'
    else:
        current_cs = sorted(S, key=len)[0]
        var = find_max_var(ft, current_cs)
        return var, PaDAprob(ft, remove_cs(S, var)), PaDAprob(ft, remove_var(S, var))

def find_max_var(ft, current_cs):
    """
    Function to find the event with the lowest probability within a cut set
    :param ft: fault tree that is being used
    :param current_cs: the cut set that is currently being used
    :return: variable with the highest failure probability
    """
    prob = 0
    for var in current_cs:
        current = ft.find_vertex_by_name(ft, var)
        if current.prob > prob:
            prob = current.prob
    return var


def find_min_path_set(ft, S):
    """
    Function that calculates probability of all path sets and returns the one with the lowest probability
    :param ft: fault tree
    :param S: set of cut sets
    :return: cut set in S with the lowest probability
    """
    maxP = 0
    cutset = None
    for cs in S:
        P = 1
        for vertex in cs:
            current = ft.find_vertex_by_name(ft, vertex)
            P *= (1-current.prob)
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

    S = top.path_set(top)
    probDDT = PaDAprob(top, S)
    sizeDDT = PaDAsize(top, S)
    print("prob:", probDDT)
    print("size:", sizeDDT)