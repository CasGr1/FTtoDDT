from FaultTree.FT import *
from FaultTree.FTParser import *
from DDT.DDT import *

def WorstCost(ft):
    """
    This is an algorithm for transforming fault trees to diagnostic decision trees using a bottom-up approach
    :param ft: the fault tree that needs to be performed
    :return: diagnostic decision tree
    """
    if ft.type == FtElementType.BE:
        return 1

    if ft.type == FtElementType.AND:
        if ft.children[0].prob <= ft.children[1].prob:
            # print("1: " + ft.children[0].name + " / " + ft.children[1].name)
            return WorstCost(ft.children[0])/ft.children[1].prob
        else:
            # print("2: " + ft.children[1].name + " / " + ft.children[0].name)
            return WorstCost(ft.children[1])/ft.children[0].prob

    if ft.type == FtElementType.OR:
        if ft.children[0].prob <= ft.children[1].prob:
            # print("3: " + ft.children[0].name + " / 1- " + ft.children[1].name)
            return WorstCost(ft.children[1])/(1-ft.children[0].prob)
        else:
            # print("4: " + ft.children[1].name + " / 1- " + ft.children[0].name)
            return WorstCost(ft.children[0])/(1-ft.children[1].prob)


if __name__ == "__main__":

    FT.unreliability(add_unreliability=True)
    print(WorstCost(top))

