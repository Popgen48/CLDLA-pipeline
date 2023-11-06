import sys

def compare(f1, f2): # f1 is test, f2 is truth
    identical = True
    with open(f1, 'r') as file1, open(f2, 'r') as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()
    
        # compare the lines of each file
        for i, (line1, line2) in enumerate(zip(file1_lines, file2_lines)):
            line1 = line1.strip().split()
            line2 = line2.strip().split()
            if f1.endswith(".hap"):
                hap = []
                for item in line1:
                    hap.extend((list(item)))
                line1 = hap
            if f1.endswith(".par"):
                line2 = line2[0]
            if line1 != line2:
                identical = False
                print(f"Files differ at line {i+1}:")
                print(f"File 1: {line1.strip()}")
                print(f"File 2: {line2.strip()}")
                print("-------------")
                #break
        if identical:
            print(f"Files {f1} and {f2} are identical")

for i in [".hap", ".map", ".par"]:
    # f1 is test, f2 is truth
    f1 = sys.argv[1] + i
    f2 = sys.argv[2] + i
    compare(f1, f2)