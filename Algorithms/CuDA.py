from FaultTree.FT import *

def CuDA(ft, S):
    if not S:
        return '0'
    if [] in S:
        return '1'
    else:
        current_cs = find_likely_cut_set(ft, S)
        var = find_min_var(ft, current_cs)
        return (var, CuDA(ft, remove_cs(S, var)), CuDA(ft, remove_var(S, var)))

def remove_var(cutsets, event_to_remove):
    updated_cutsets = [
        [e for e in cutset if e != event_to_remove]
        for cutset in cutsets
    ]
    return updated_cutsets

def remove_cs(cutsets, event):
    updated_cutsets = [cutset for cutset in cutsets if event not in cutset]
    return updated_cutsets
def find_min_var(ft, current_cs):
    prob = float('inf')
    for var in current_cs:
        current = ft.find_vertex_by_name(ft, var)
        if current.prob < prob:
            prob = current.prob
    return var

def find_likely_cut_set(ft, S):
    maxP = 0
    cutset = None
    for cs in S:
        P = 1
        for vertex in cs:
            current = ft.find_vertex_by_name(ft, vertex)
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
    print(CuDA(top, S))