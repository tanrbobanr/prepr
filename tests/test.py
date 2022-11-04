import sys
sys.path.append(".")
from src import prepr
sys.setrecursionlimit(100)

class TESTCLASS:
    def __init__(self, a, b, c = None) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.e = None
    def __repr__(self, *args, **kwargs) -> prepr.types.pstr:
        return prepr.prepr(self).args(self.a, self.b).kwargs(None, c = self.c
            ).attr("e", self.e, None).build(*args, **kwargs)


inst = TESTCLASS(1, None, "C")
inst.e = TESTCLASS([1, 2, inst], {'a':1, 'b':2, 'c':3})
inst.e.e = inst

print(inst)

