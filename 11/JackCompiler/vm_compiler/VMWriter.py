import os
from xml_compiler import JackAnalyser


self_path = "/home/mkl/Dropbox/Datamatiker/4semester/IoT/JackCompiler/vm_compiler"
move_path = "/home/mkl/Dropbox/Datamatiker/4semester/IoT/JackCompiler/vm_compiler/vm_testing"

class VMWriter():
    def __init__(self, xml_file):
        self.filename, ext = os.path.splitext(xml_file)
        self.output = self.filename + ".vm"
        self.file = open(self.output, "w+")

    def write_push(self, segment, index):
        self.file.write("push " + segment + " " + str(index) + "\n")


    def write_pop(self, segment, index):
        self.file.write("pop " + segment + " " + str(index) + "\n")

    def write_arithmetic(self, command):
        self.file.write(command + "\n")

    def write_call(self, name, n_args):
        self.file.write("call " + name + " " + str(n_args) + "\n")

    def write_label(self, label):
        self.file.write("label " + label + "\n")

    def write_if_goto(self, label):
        self.file.write("if-goto " + label + "\n")

    def write_goto(self, label):
        self.file.write("goto " + label + "\n")

    def write_return(self):
        self.file.write("return \n")
    #here
    def write_function(self, name, n_locals):
        self.file.write(name + " " + str(n_locals) + "\n")
        #self.write_push("argument", 0)
        #self.write_pop("pointer", 0)

    def close(self):
        self.file.close()
        #JackAnalyser._override_move_file(self.output, self_path + "/" + self.output, move_path)
        return self.output
