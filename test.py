from FaultTree.FTParser import *
from DDT.DDT import *
from Algorithms.WorstCaseCalc import *
from Algorithms.Cost.EDAcost import *
from Algorithms.Height.BUDA import *
from Algorithms.Cost.BUDAcost import *
from Tests.CompareFTtoDDT import *
from Algorithms.Cost.BUDAcostWORST import *


if __name__ == "__main__":
    FTfile = "FaultTree/FTexamples/FFORTcost/csdcost.dft"
    FaultTree = FTParse(FTfile)

    FaultTree.unreliability(add_unreliability=True)
    B = FaultTree.variables()
    P = FaultTree.probabilities()
    S = FaultTree.cut_set()
    C = FaultTree.cost_dict()
    Pathsets = FaultTree.path_set()
    # FaultTree.print()

    print("Worst cost ratio:", WorstCost(FaultTree))
    
    # EDADDT, EDAcost = EDAcost(FaultTree, B, P, C)
    # print("EDA cost:", EDAcost)
    # BUDA
    BUDADDT, crap, scrap2 = BUDAcost(FaultTree)
    BUDAfinalDDT = ddt_from_tuple(BUDADDT, P, C)
    # BUDAfinalDDT.print()
    print("BUDA Exp Height:", BUDAfinalDDT.expected_cost())
    print(compare_ft_to_ddt(BUDAfinalDDT, FaultTree))
    #
    # # BUDA
    # BUDADDTp = BUDA(FaultTree)
    # BUDAfinalDDTp = ddt_from_tuple(BUDADDTp, P, C)
    # # BUDAfinalDDTp.print()
    # print("BUDAp Exp Height:", BUDAfinalDDTp.expected_cost())
    # print(compare_ft_to_ddt(BUDAfinalDDTp, FaultTree))
    #
    # # BUDA
    # BUDADDTw, wscrap, wscrap2 = BUDAcostworst(FaultTree)
    # BUDAfinalDDTw = ddt_from_tuple(BUDADDTw, P, C)
    # # BUDAfinalDDT.print()
    # print("BUDAw Exp Height:", BUDAfinalDDTw.expected_cost())
    # print(compare_ft_to_ddt(BUDAfinalDDTw, FaultTree))