import sys
from util import compare

for i in [".hap", ".map", ".par"]:
    # f1 is test, f2 is truth
    f1 = sys.argv[1] + i
    f2 = sys.argv[2] + i
    compare(f1, f2)