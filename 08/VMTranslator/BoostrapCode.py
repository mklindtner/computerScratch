import os, shutil
import numpy as np
from Parser import Parser


def initialize_pointer():
    cover_shit = []
    build_assembly = []
    build_assembly.append("@256")
    build_assembly.append("D=A")
    build_assembly.append("@SP")
    build_assembly.append("M=D")
    cover_shit.append(build_assembly)
    cover_shit.append(_registers_for_testing(build_assembly))
    return cover_shit

def _registers_for_testing(build_assembly):
    #LCL
    build_assembly.append("@317")
    build_assembly.append("D=A")
    build_assembly.append("@LCL")
    build_assembly.append("M=D")
    #ARG
    build_assembly.append("@310")
    build_assembly.append("D=A")
    build_assembly.append("@ARG")
    build_assembly.append("M=D")
    # HEAP
    # THIS
    build_assembly.append("@3000")
    build_assembly.append("D=A")
    build_assembly.append("@THIS")
    build_assembly.append("M=D")
    # THAT
    build_assembly.append("@4000")
    build_assembly.append("D=A")
    build_assembly.append("@THAT")
    build_assembly.append("M=D")


def _write_debug_file(filename, test_file):
    a = np.array(test_file)
    with open(filename, "w") as fw:
        for expr in a:
            if expr is None:
                continue
            for x in range(0, len(expr)):
                if type(expr[x]) == int:
                    fw.write(str(expr))
                else:
                    for single_expression in expr[x]:
                        fw.write(single_expression + "\n")

def run_through_dir(item):
    file_list = os.listdir(item)
    list_file_vm = []
    for file in file_list:
        filename, file_ext = os.path.splitext(file)
        if file_ext == ".vm":
            list_file_vm.append(file)

    program_file, test_file = sort_vm_list(list_file_vm, item)
    _write_hack_file(os.path.basename(item)+".asm", program_file)
    _write_debug_file("tester_for_file.asm", test_file)

def sort_vm_list(vm_files, item):
    full_program = []
    full_program_debug = []
    if "Sys.vm" in vm_files:
        idx_sys = vm_files.index("Sys.vm")
        sys_val = vm_files.pop(idx_sys)
        vm_files.insert(0, sys_val)

    first_line = True
    for file in vm_files:
        full_name = item + "/" + file
        if first_line:
            #full_program.append(initialize_pointer())
            first_line = False
        curr_parser = Parser(full_name)
        prog, test_prog = curr_parser.read_file()
        full_program.append(prog)
        full_program_debug.append(test_prog)
    return full_program, full_program_debug


def file_or_directory(item):
    filename, file_ext = os.path.splitext(item)
    if not file_ext:
        run_through_dir(item)
    else:
        print("run simple code")


def _write_hack_file(file_asm_hack, hack_program):
    a = np.array(hack_program)
    with open(file_asm_hack, "w") as fw:
        for expr in a:
            for x in range(0, len(expr)):
                if expr[x]:
                    for single_expression in expr[x]:
                        #print(single_expression)
                        fw.write(single_expression + "\n")

def _move_file_to_dist(src, dest):
    shutil.move(src, dest)

#file_or_directory("/home/mkl/Dropbox/Datamatiker/4semester/IoT/nand2tetris-emu/projects/08/FunctionCalls/StaticsTest")
#_move_file_to_dist("/home/mkl/Dropbox/Datamatiker/4semester/IoT/VMTranslator/StaticsTest.asm", "/home/mkl/Dropbox/Datamatiker/4semester/IoT/nand2tetris-emu/projects/08/FunctionCalls/StaticsTest")
#file_or_directory("/home/mkl/Dropbox/Datamatiker/4semester/IoT/VMTranslator")


#file_or_directory("/home/mkl/Dropbox/Datamatiker/4semester/IoT/nand2tetris-emu/projects/07/MemoryAccess/BasicTest")
file_or_directory("/home/mkl/Dropbox/Datamatiker/4semester/IoT/nand2tetris-emu/projects/08/ProgramFlow/FibonacciSeries")
