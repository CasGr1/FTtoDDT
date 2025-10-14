from Algorithms.WorstCaseCalc import *
from Algorithms.Cost.BUDAcost import *
from Algorithms.Height.BUDA import *
import os


if __name__ == "__main__":
    folder = "FaultTree/FTexamples/FFORTbinarycost"
    results = {}
    for fname in os.listdir(folder):
        full_path = os.path.join(folder, fname)
        if os.path.isfile(full_path) and fname.endswith(".dft"):
            FaultTree = FTParse(full_path)
            FaultTree.unreliability(add_unreliability=True)


            cost = WorstCost(FaultTree)
            print(fname + ": " + str(cost))

            BUDAc = ddt_from_tuple(BUDAcost(FaultTree)[0], FaultTree.probabilities(), FaultTree.cost_dict()).expected_cost()
            BUDAp = ddt_from_tuple(BUDA(FaultTree), FaultTree.probabilities(), FaultTree.cost_dict()).expected_cost()
            fBUDAc = ddt_from_tuple(BUDAcost(FaultTree)[0], FaultTree.probabilities(), FaultTree.cost_dict()).expected_cost_failure()
            fBUDAp = ddt_from_tuple(BUDA(FaultTree), FaultTree.probabilities(), FaultTree.cost_dict()).expected_cost_failure()
            print(fname + " BUDAc: " + str(BUDAc) + " BUDAp: " + str(BUDAp) + "")
            print(fname + " BUDAc: " + str(fBUDAc) + " BUDAp: " + str(fBUDAp) + "\n")
            results[fname] = cost
    # print(results)