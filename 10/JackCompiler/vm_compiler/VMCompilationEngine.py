from vm_compiler import CopyXMLcompilationEngine


class VMCE():

    def __init__(self, input, output):
        self.input = input
        self.output = output


    def compile(self):
        CopyXMLcompilationEngine.CompilationEngine(self.input, self.output)


