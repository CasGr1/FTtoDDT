from Algorithms.Cost.EDAcost import *
from Algorithms.Cost.BUDAcost import *
from Algorithms.Cost.CuDAcost import *
from FaultTree.FTParser import *
from DDT.DDT import *
from timeit import default_timer as timer
from Tests.CompareFTtoDDT import *


def prep(filename):
    FaultTree = FTParse(filename)
    FaultTree.unreliability(add_unreliability=True)
    B = FaultTree.variables()
    P = FaultTree.probabilities()
    S = FaultTree.cut_set()
    Pathsets = FaultTree.path_set()
    cost = FaultTree.cost_dict()
    return FaultTree, B, P, S, Pathsets, cost

if __name__ == "__main__":
    # Get all needed from Fault Tree
    FaultTree, B, P, S, Pathsets, cost = prep("FaultTree/FTexamples/Cost/Aircraft(FT4)COST.dft")

    Testname = "AircraftBUDAtest.txt"
    total_time = 0.0

    with open("Results/" + Testname, "w") as f:
        for i in range(0,25, 1):
            # Timing algorithms
            start = timer()
            testddt, dep, depr = BUDAcost(FaultTree)
            end = timer()
            total_time += end - start

            # Check if ddt is correct
            final = ddt_from_tuple(testddt, P)
            correct = compare_ft_to_ddt(final, FaultTree)
            height= final.expected_height()
            f.write(f"test {i} (s): {end - start, correct} Exp Height: {height} \n")
        f.write(f"Average time: {total_time/10}")


