from Algorithms.Cost.EDAcost import *
from Algorithms.Cost.BUDAcost import *
from Algorithms.Cost.CuDAcost import *
from Algorithms.Cost.PaDAcost import *
from Algorithms.Cost.DIFcost import *
from Algorithms.Height.BUDA import *
from Algorithms.Height.CuDA import *
from Algorithms.Height.PaDA import *
from FaultTree.FTParser import *
from DDT.DDT import *
import matplotlib.pyplot as plt
import numpy as np
import os


def prep(filename):
    FaultTree = FTParse(filename)
    FaultTree.unreliability(add_unreliability=True)
    B = FaultTree.variables()
    P = FaultTree.probabilities()
    S = FaultTree.cut_set()
    Pathsets = FaultTree.path_set()
    cost = FaultTree.cost_dict()
    return FaultTree, B, P, S, Pathsets, cost

def plot_exp_cost(data_dicts, title="Comparison of Methods"):
    """
    Plot grouped bar chart for multiple dictionaries.

    Args:
        data_dicts (dict): A dictionary where keys are dataset names (e.g., "CUDA", "BUDA")
                           and values are dictionaries with the same keys and numeric values.
        title (str): Title of the plot.
    """
    # Extract dataset names and ensure all share the same keys
    dataset_names = list(data_dicts.keys())
    keys = list(next(iter(data_dicts.values())).keys())
    x = np.arange(len(keys))

    # Bar width adjusted dynamically
    n = len(dataset_names)
    width = 0.8 / n

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (name, dct) in enumerate(data_dicts.items()):
        values = [dct.get(k, 0) for k in keys]
        ax.bar(x + (i - n/2) * width + width/2, values, width, label=name)

    # Labels and title
    ax.set_xticks(x)
    ax.set_xticklabels(keys, rotation=20)
    ax.set_ylabel("Values")
    ax.set_title(title)
    ax.legend()

    plt.tight_layout()
    plt.show()

def cost(ddt, failure):
    if failure == False:
        return ddt.expected_cost()
    elif failure == True:
        return ddt.expected_cost_failure()

if __name__ == "__main__":
    CUDA_cost = {}
    CUDA_prob = {}
    PADA_cost = {}
    PADA_prob = {}
    BUDA_cost = {}
    BUDA_prob = {}
    DIF_cost  = {}
    EDA_cost  = {}
    folder = "../FaultTree/FTexamples/FFORTcost"
    fail = True

    for fname in os.listdir(folder):
        full_path = os.path.join(folder, fname)
        if os.path.isfile(full_path) and fname.endswith(".dft"):
            file = os.path.basename(full_path)
            print(file)
            ft, var, prob, cs, ps, cst = prep(full_path)
            # if file == "ptCOST.dft" or file == "csdcost.dft" or file == "testBigDIFF.dft":
            #     EDAddt, EDAexpcost = EDAcost(ft, var, prob, cst)
            #     EDAdict[file] = EDAexpcost
            #
            #     # worst, worstexpcost = EDAworst(ft, var, prob, cst)
            #     # worstdict[file] = worstexpcost

            BUDApddt = BUDA(ft)
            BUDApconvertedddt = ddt_from_tuple(BUDApddt, prob, cst)
            BUDA_prob[file] = cost(BUDApconvertedddt, fail)

            BUDAddt, adf, sdf = BUDAcost(ft)
            BUDAconvertedddt = ddt_from_tuple(BUDAddt, prob, cst)
            BUDA_cost[file] = cost(BUDAconvertedddt, fail)

            PaDApddt = PaDAprob(ft, ps)
            paDApconvertedddt = ddt_from_tuple(PaDApddt, prob, cst)
            PADA_prob[file] = cost(paDApconvertedddt, fail)

            PaDAddt = PaDAcost(ft, ps)
            paDAconvertedddt = ddt_from_tuple(PaDAddt, prob, cst)
            PADA_cost[file] = cost(paDAconvertedddt, fail)

            CuDApddt = CuDAprob(ft, cs)
            CuDApconvertedddt = ddt_from_tuple(CuDApddt, prob, cst)
            CUDA_prob[file] = cost(CuDApconvertedddt, fail)

            CuDAddt = CuDAcost(ft, cs)
            CuDAconvertedddt = ddt_from_tuple(CuDAddt, prob, cst)
            CUDA_cost[file] = cost(CuDAconvertedddt, fail)

            DIFddt = DIDACOST(ft, cs)
            DIFconvertedddt = ddt_from_tuple(DIFddt, prob, cst)
            DIF_cost[file] = cost(DIFconvertedddt, fail)

    plot_exp_cost({"CUDAcost": CUDA_cost,
                   "CUDAprob": CUDA_prob,
                   "PADAcost": PADA_cost,
                   "PADAprob": PADA_prob,
                   "BUDAcost": BUDA_cost,
                   "BUDAprob": BUDA_prob,
                   "DIF":      DIF_cost
                   })
