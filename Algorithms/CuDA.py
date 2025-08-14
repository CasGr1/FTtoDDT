from FaultTree.FT import *

def CuDA(ft, S):
    if S is empty:
        return '0'
    elif S is :
        return '1'
    else:
        current_cs = find_likely_cut_set(ft, S)
        

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
    print(S)
    print(find_likely_cut_set(top, S))