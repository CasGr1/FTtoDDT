from Algorithms.Cost.EDAcost import *
from Algorithms.Cost.BUDAcost import *
from Algorithms.Cost.CuDAcost import *
from Algorithms.Cost.DIFcost import *
from Algorithms.Height.CuDA import *
from FaultTree.FTParser import *
from DDT.DDT import *
import matplotlib.pyplot as plt
import numpy as np


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


if __name__ == "__main__":
    CUDA_exp_cost_dict = {}
    CUDA_normal = {}
    BUDA_exp_cost_dict = {}
    DIF_exp_cost_dict = {}
    EDAdict = {}
    Filenames = ["Aircraft(FT4)COST.dft", "mpsCOST.dft", "ptCOST.dft", "PCBAcost.dft", "csdcost.dft", "ATC(FT3)cost.dft"]

    for file in Filenames:
        ft, var, prob, cs, ps, cst = prep("FaultTree/FTexamples/Cost/" + file)
        if file == "ptCOST.dft" or file == "csdcost.dft":
            EDAddt, EDAexpcost = EDAcost(ft, var, prob, cst)
            EDAdict[file] = EDAexpcost

        BUDAddt, adfs, asdf = BUDAcost(ft)
        BUDAconvertedddt = ddt_from_tuple(BUDAddt, prob, cst)
        BUDA_exp_cost_dict[file] = BUDAconvertedddt.expected_cost()
        print(BUDA_exp_cost_dict[file])

        Cnormal = CuDAprob(ft, cs)
        Cnormalconverted = ddt_from_tuple(Cnormal, prob, cst)
        CUDA_normal[file] = Cnormalconverted.expected_cost()


        CuDAddt = CuDAcost(ft, cs)
        CuDAconvertedddt = ddt_from_tuple(CuDAddt, prob, cst)
        CUDA_exp_cost_dict[file] = CuDAconvertedddt.expected_cost()
        print(CUDA_exp_cost_dict[file])

        DIFddt = DIDACOST(ft, cs)
        DIFconvertedddt = ddt_from_tuple(DIFddt, prob, cst)
        DIF_exp_cost_dict[file] = DIFconvertedddt.expected_cost()
    print(f"CUDA: {CUDA_exp_cost_dict}")
    print(f"BUDA: {BUDA_exp_cost_dict}")
    print(f"DIF: {DIF_exp_cost_dict}")
    plot_exp_cost({"CUDAcost": CUDA_exp_cost_dict,
                   "CUDAprob": CUDA_normal,
                   "BUDA": BUDA_exp_cost_dict,
                   "DIF": DIF_exp_cost_dict,
                   "EDA": EDAdict})
