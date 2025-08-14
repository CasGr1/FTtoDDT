from FaultTree.FT import *
def FTParse(filename):
    fts = {}
    with open(filename, "r") as file:
        for line in file:
            line = line.strip().replace('"', '').replace(';', '')
            linelist = line.split()
            if "toplevel" in linelist[0]:
                top = linelist[1]
            name = linelist[0]
            if "or" in linelist[1]:
                FTtype = FtElementType.OR
                children = linelist[2:]

                ft_node = FT(name, FTtype, children)
                fts[name] = ft_node
            elif "and" in linelist[1]:
                FTtype = FtElementType.AND
                children = linelist[2:]

                ft_node = FT(name, FTtype, children)
                fts[name] = ft_node
            elif "prob" in linelist[1]:
                prob = float(linelist[1].split('=')[1])
                ft_node = FT(name, FtElementType.BE, prob=prob)
                fts[name] = ft_node
    for node in fts.values():
        node.children = [fts[child_name] for child_name in node.children if child_name in fts]
    return fts[top]




if __name__ == "__main__":
    FTfile = "FTexamples/loss_container_port(FT9).dft"
    # with open(FTfile) as f:
    #     print(f.read())
    FaultTree = FTParse(FTfile)
    FaultTree.print()


    # print(cut_set(FaultTree))
    # print(unreliability(FaultTree))
    # print_cut_sets(mcs)
