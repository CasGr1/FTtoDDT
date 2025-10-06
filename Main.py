from FaultTree.FTParser import *
from DDT.DDT import *
from Algorithms.Height.EDA import *
from Algorithms.Height.BUDA import *
from Algorithms.Height.CuDA import *
from Algorithms.Height.PaDA import *
from Algorithms.Height.DIF import *
from Algorithms.Cost.EDAcost import *
from Algorithms.Cost.BUDAcost import *
from Algorithms.Cost.CuDAcost import *
from Tests.CompareFTtoDDT import *

if __name__ == "__main__":
    FTfile = "FaultTree/FTexamples/HSC(FT14).dft"
    FaultTree = FTParse(FTfile)


    FaultTree.unreliability(add_unreliability=True)
    B = FaultTree.variables()
    P = FaultTree.probabilities()
    S = FaultTree.cut_set()
    Pathsets = FaultTree.path_set()
    # FaultTree.print()

    # # EDA
    # EDAddt, height = EDA(FaultTree, B, P)
    # EDAfinalddt = ddt_from_tuple(EDAddt, P)
    # print("EDA Exp Height:", height)
    # print(compare_ft_to_ddt(EDAfinalddt, FaultTree))

    # BUDA
    BUDADDT = ddt_from_tuple(BUDA(FaultTree), P)
    BUDADDT.print()
    print("BUDA Exp Height:", BUDADDT.expected_height())
    print(compare_ft_to_ddt(BUDADDT, FaultTree))

    # DIDA
    DIDADDT = ddt_from_tuple(DIDA(FaultTree, S), P)
    # DIDADDT.print()
    print("DIF Exp Height:", DIDADDT.expected_height())
    print(compare_ft_to_ddt(DIDADDT, FaultTree))

    # CuDA
    CUDAprobDDT = ddt_from_tuple(CuDAprob(FaultTree, S), P)
    # CUDAprobDDT.print()
    print("CUDAprob Exp Height:", CUDAprobDDT.expected_height())
    print(compare_ft_to_ddt(CUDAprobDDT, FaultTree))

    CUDAsizeDDT = ddt_from_tuple(CuDAsize(FaultTree, S), P)
    # print("CUDAsize DDT:", CUDAsizeDDT)
    print("CUDAsize Exp Height:", CUDAsizeDDT.expected_height())
    print(compare_ft_to_ddt(CUDAsizeDDT, FaultTree))

    # PaDA
    PADAprobDDT = ddt_from_tuple(PaDAprob(FaultTree, Pathsets), P)
    # print("PADAprob DDT:", PADAprobDDT)
    print("PADAprob Exp Height:", PADAprobDDT.expected_height())
    print(compare_ft_to_ddt(PADAprobDDT, FaultTree))

    PADAsizeDDT = ddt_from_tuple(PaDAsize(FaultTree, Pathsets), P)
    # print("PADAsize DDT:", PADAsizeDDT)
    print("PADAsize Exp Height:", PADAsizeDDT.expected_height())
    print(compare_ft_to_ddt(PADAsizeDDT, FaultTree))