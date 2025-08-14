from FaultTree.FTParser import *
from Algorithms.EDA import *
from Algorithms.BUDA import *

if __name__ == "__main__":
    FTfile = "FaultTree/FTexamples/loss_container_port(FT9).dft"
    FaultTree = FTParse(FTfile)
    # FaultTree.print()

    FaultTree.unreliability(add_unreliability=True)
    B = FaultTree.variables(FaultTree)
    P = FaultTree.probabilities(FaultTree)
    # print(B)
    # print(P)

    #EDA
    # ddt, height = EDA(FaultTree, B, P)
    # print("EDA DDT:", ddt)
    # print("EDA Exp Height:", height)

    #BUDA
    DDT = BUDA(FaultTree)
    print("BUDA DDT:", DDT)
    print("BUDA Exp Height:", expected_height(DDT, P))