from FaultTree.FTParser import *
from Algorithms.EDA import *
from Algorithms.BUDA import *
from Algorithms.CuDA import *
from Algorithms.PaDA import *


if __name__ == "__main__":
    FTfile = "FaultTree/FTexamples/csd.dft"
    FaultTree = FTParse(FTfile)
    # FaultTree.print()

    FaultTree.unreliability(add_unreliability=True)
    B = FaultTree.variables(FaultTree)
    P = FaultTree.probabilities(FaultTree)
    S = FaultTree.cut_set(FaultTree)
    # print(B)
    # print(P)

    # EDA
    EDAddt, height = EDA(FaultTree, B, P)
    print("EDA DDT:", EDAddt)
    print("EDA Exp Height:", height)

    #BUDA
    BUDADDT = BUDA(FaultTree)
    print("BUDA DDT:", BUDADDT)
    print("BUDA Exp Height:", expected_height(BUDADDT, P))

    #CUDA
    CUDADDT = CuDA(FaultTree, S)
    print("CUDA DDT:", CUDADDT)
    print("CUDA Exp Height:", expected_height(CUDADDT, P))

    # CUDA
    PADADDT = PaDA(FaultTree, S)
    print("PADA DDT:", PADADDT)
    print("PADA Exp Height:", expected_height(PADADDT, P))
