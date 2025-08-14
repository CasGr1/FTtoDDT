from FaultTree.FT import *

def EDA(ft, B, P):
    if ft_false(ft):
        return '0', 0
    if ft_true(ft):
        return '1', 0

    opt_height = float('inf')
    opt_tree = None

    for b in B:
        B_new = B - {b}
        f0 = restrict(ft, b, 0)
        f1 = restrict(ft, b, 1)

        D0, h0 = EDA(f0, B_new, P)
        D1, h1 = EDA(f1, B_new, P)

        # Add line for expected height
        h = 1 + (1-P[b])*h0 + P[b]*h1

        if h < opt_height:
            opt_height = h
            opt_tree = (b, D0, D1)

    return opt_tree, opt_height

def restrict(ft, b, val):
    if ft.type == FtElementType.BE:
        if ft.name == b:
            return FT(ft.name, FtElementType.BE, prob = val)
        else:
            return ft

    new_children = [restrict(child, b, val) for child in ft.children]

    if all(child.type == FtElementType.BE and child.probabilities in [0, 1] for child in new_children):
        if ft.type == FtElementType.AND:
            if any(child.prob == '0' for child in new_children):
                return FT('ZERO', FtElementType.BE, prob=0)
            else:
                return FT('ONE', FtElementType.BE, prob=1)
        elif ft.type == FtElementType.OR:
            if any(child.prob == 1 for child in new_children):
                return FT('ONE', FtElementType.BE, prob=1)
            else:
                return FT('ZERO', FtElementType.BE, prob=0)

    return FT(ft.name, ft.type, new_children)

def ft_false(ft):
    if ft.type == FtElementType.BE:
        return ft.prob == 0
    if ft.type == FtElementType.AND:
        return any(ft_false(child) for child in ft.children)
    if ft.type == FtElementType.OR:
        return all(ft_false(child) for child in ft.children)

def ft_true(ft):
    if ft.type == FtElementType.BE:
        return ft.prob == 1
    if ft.type == FtElementType.AND:
        return all(ft_true(child) for child in ft.children)
    if ft.type == FtElementType.OR:
        return any(ft_true(child) for child in ft.children)


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

    B = top.variables(top)
    P = top.probabilities(top)

    ddt, height = EDA(top, B, P)
    print("DDT:", ddt)
    print("Exp height:", height)

    from Algorithms.BUDA import expected_height
    print(expected_height(ddt, P))



