from Old import Instructions as assm_ins
import os

program = []


def convert_to_binary(file):
    with open(file, "r") as f:
        for line in f:
            if "//" in line:
                continue
            advance(line)
    file_write = change_ext_to_asm(file)
    with open(file_write, "w") as fw:
        for line in program:
            fw.write(line+"\n")


def advance(line):
    program.append(assm_ins.InstructionToBinary(line.strip()))
    #print("line: " + line)

def change_ext_to_asm(file):
    filename, file_ext = os.path.splitext(file)
    return filename + ".hack"

convert_to_binary(os.sys.argv[1])




def hasMoreCommands(file):
    return None
    #check if EoF
    #readLine() here and call advance if line is not empty or "//"?


def commandType():
    return None
