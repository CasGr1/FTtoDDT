from enum import Enum

class DdtElementType(Enum):
    DEC = 1
    ONE = 2
    ZERO = 3


class DDT:
    def __init__(self, name, DdtElement, children = None, prob=0):
        if children == None:
            children = []
        self.name = name
        self.type = DdtElement
        self.children = children
        self.prob = prob


    def print(self):
        print(self.to_string())

    def to_string(self, level=0):
        indent = "  " * level
        result = f"{indent}- {self.name} (type: {self.type}, prob: {self.prob})\n"
        for child in self.children:
            result += child.to_string(level + 1)
        return result


if __name__ == "__main__":
    ONE = DDT("ONE", DdtElementType.ONE)
    ZERO = DDT("ZERO", DdtElementType.ZERO)
    dec = DDT("BE1", DdtElementType.DEC, [ONE, ZERO])
    dec.print()
