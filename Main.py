from FaultTree.FTParser import *
from Algorithms.Height.EDA import *
from Algorithms.Height.BUDA import *
from Algorithms.Height.CuDA import *
from Algorithms.Height.PaDA import *
from Algorithms.Height.DIF import *

if __name__ == "__main__":
    FTfile = "FaultTree/FTexamples/loss_container_port(FT9).dft"
    FaultTree = FTParse(FTfile)
    # FaultTree.print()

    FaultTree.unreliability(add_unreliability=True)
    B = FaultTree.variables()
    P = FaultTree.probabilities()
    S = FaultTree.cut_set()
    Pathsets = FaultTree.path_set()
    # print(B)
    # print(P)

    # EDA
    # EDAddt, height = EDA(FaultTree, B, P)
    # print("EDA DDT:", EDAddt)
    # print("EDA Exp Height:", height)

    # BUDA
    BUDADDT = BUDA(FaultTree)
    print("BUDA DDT:", BUDADDT)
    print("BUDA Exp Height:", expected_height(BUDADDT, P))

    # DIDA
    DIDADDT = DIDA(FaultTree, S)
    print("DIF DDT:", DIDADDT)
    print("DIF Exp Height:", expected_height(DIDADDT, P))

    # CuDA
    CUDAprobDDT = CuDAprob(FaultTree, S)
    print("CUDAprob DDT:", CUDAprobDDT)
    print("CUDAprob Exp Height:", expected_height(CUDAprobDDT, P))

    CUDAsizeDDT = CuDAsize(FaultTree, S)
    print("CUDAsize DDT:", CUDAsizeDDT)
    print("CUDAseize Exp Height:", expected_height(CUDAsizeDDT, P))

    # PaDA
    PADAprobDDT = PaDAprob(FaultTree, Pathsets)
    print("PADAprob DDT:", PADAprobDDT)
    print("PADAprob Exp Height:", expected_height(PADAprobDDT, P))

    PADAsizeDDT = PaDAsize(FaultTree, Pathsets)
    print("PADAsize DDT:", PADAsizeDDT)
    print("PADAsize Exp Height:", expected_height(PADAsizeDDT, P))
    