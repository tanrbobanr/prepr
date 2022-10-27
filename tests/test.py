import sys
sys.path.append(".")
from src import prepr

class TESTCLASS:
    def __init__(self, a, b, c = None) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.e = None
    def __repr__(self) -> prepr.types.prepr_str:
        return prepr.prepr(self).args(self.a, self.b).kwargs(None, c = self.c).attr("e", self.e, None).build()


inst = TESTCLASS(1, None, "C")
inst.e = TESTCLASS([1, 2, 3], {'a':1, 'b':2, 'c':3})
inst.e.e = inst

print(inst)

