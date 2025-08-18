from FaultTree.FT import *
from Algorithms.Height.CuDA import remove_cs, remove_var

def PaDAprob(ft, S):
    """
    This is an algorithm that transforms fault trees into diagnostic decision trees using path sets
    It picks the path sets based on probability
    :param ft: fault tree that will be converted
    :param S: a set of all minimal cut sets
    :return: a diagnostic decision tree corresponding to ft
    """

    if not S:
        return '1'
    if [] in S:
        return '0'
    else:
        current_ps = find_min_path_set(ft, S)
        var = find_max_var(ft, current_ps)
        return var, PaDAprob(ft, remove_var(S, var)), PaDAprob(ft, remove_cs(S, var))


def PaDAsize(ft, S):
    """
    This is an algorithm that transforms fault trees into diagnostic decision trees using path sets
    It picks path sets based on size
    :param ft: fault tree that will be converted
    :param S: a set of all minimal cut sets
    :return: a diagnostic decision tree corresponding to ft
    """

    if not S:
        return '1'
    if [] in S:
        return '0'
    else:
        current_ps = sorted(S, key=len)[0]
        var = find_max_var(ft, current_ps)
        return var, PaDAprob(ft, remove_var(S, var)), PaDAprob(ft, remove_cs(S, var))

def find_max_var(ft, current_ps):
    """
    Function to find the event with the highest probability within a cut set
    :param ft: fault tree that is being used
    :param current_cs: the cut set that is currently being used
    :return: variable with the highest failure probability
    """
    prob = 0
    max_var = None
    for var in current_ps:
        current = ft.find_vertex_by_name(var)
        if current.prob > prob:
            prob = current.prob
            max_var = current.name
    return max_var


def find_min_path_set(ft, S):
    """
    Function that calculates probability of all path sets and returns the one with the lowest probability
    :param ft: fault tree
    :param S: set of cut sets
    :return: path set in S with the lowest probability
    """
    maxP = 0
    pathset = None
    for ps in S:
        P = 1
        for vertex in ps:
            current = ft.find_vertex_by_name(vertex)
            P *= (1-current.prob)
        if P > maxP:
            maxP = P
            pathset = ps
    return pathset


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

    S = top.path_set()
    probDDT = PaDAprob(top, S)
    sizeDDT = PaDAsize(top, S)
    print("prob:", probDDT)
    print("size:", sizeDDT)
    from Algorithms.Height.BUDA import expected_height
    print(expected_height(probDDT, top.probabilities()))