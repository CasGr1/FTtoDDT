from FaultTree.FT import *

def EDA(ft, variables, probabilities):
    """
    This is an exact algorithm for transforming fault trees into diagnostic decision trees.
    It performs the transformation by calculating all possible decision trees and
    picking the one with the lowest expected height
    :param ft: Fault Tree that will be converted
    :param variables: set of variables in ft
    :param probabilites: dict of probabilities in ft, where key is the basic event and the value is the probability of failure
    :return: an optimal diagnostic decision tree corresponding to ft
    """
    if ft_false(ft):
        return '0', 0
    if ft_true(ft):
        return '1', 0

    optimal_height = float('inf')
    optimal_tree = None

    for var in variables:
        remaining_var = variables - {var}
        left_ft = restrict(ft, var, 0)
        right_ft = restrict(ft, var, 1)

        left_tree, left_height = EDA(left_ft, remaining_var, probabilities)
        right_tree, right_height = EDA(right_ft, remaining_var, probabilities)

        height = 1 + (1-probabilities[var])*left_height + probabilities[var]*right_height

        if height < optimal_height:
            optimal_height = height
            optimal_tree = (var, left_tree, right_tree)
    return optimal_tree, optimal_height

def restrict(ft, var, value):
    """
    Function that evaluates a variable in a fault tree
    :param ft: fault tree that needs to be restricted
    :param var:  variable that needs to be evaluated
    :param value: what var is evaluated to, 0 meaning non-failure and 1 meaning failure
    :return: fault tree where b is evaluated corresponding to value
    """
    if ft.type == FtElementType.BE:
        if ft.name == var:
            return FT(ft.name, FtElementType.BE, prob = value)
        else:
            return ft

    new_children = [restrict(child, var, value) for child in ft.children]

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
    """
    function that checks if all elements evaluate to non-failure
    :param ft: fault tree
    :return:
    True if fault tree evaluates to 0
    False if fault tree does not evaluate to 0
    """
    if ft.type == FtElementType.BE:
        return ft.prob == 0
    if ft.type == FtElementType.AND:
        return any(ft_false(child) for child in ft.children)
    if ft.type == FtElementType.OR:
        return all(ft_false(child) for child in ft.children)

def ft_true(ft):
    """
    function that checks if all elements evaluate to failure
    :param ft: fault tree
    :return:
    True if fault tree evaluates to 1
    False if fault tree does not evaluate to 1
    """
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



