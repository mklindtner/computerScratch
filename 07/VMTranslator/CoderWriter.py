from CommandType import CommandType
vm_to_assembly = ""
initialize_pointer = True


def write_arithmetic(command, equals_generator=None):
    build_assembly = []
    if command == 'add':
        _add_stack(build_assembly)
    elif command == 'sub':
        _sub_stack(build_assembly)
    elif command == 'neg':
        _neg_stack(build_assembly)
    #equals operator
    elif command == 'eq':
        _equals_stack(build_assembly, equals_generator, "JEQ")
    elif command == "gt":
        _equals_stack(build_assembly, equals_generator, "JGT")
    elif command == "lt":
        _equals_stack(build_assembly, equals_generator, "JLT")
    #bitwise
    elif command == "and":
        _bitwise_stack(build_assembly, "M=D&M")
    elif command == "or":
        _bitwise_stack(build_assembly, "M=D|M")
    elif command == "not":
        _bitwise_not_stack(build_assembly)
    return build_assembly


def write_push_pop(cmd_type, segment, index, filename):
    build_assembly = []
    seg_strip = segment.strip()

    if cmd_type is CommandType.C_PUSH:
        _decide_push_segment(build_assembly, seg_strip, index, filename)

    if cmd_type is CommandType.C_POP:
        _decide_pop_segment(build_assembly, seg_strip, index, filename)

    return build_assembly

#choosing to return build assembly here
def write_init():
    build_assembly = []
    #_initiate_pointers(build_assembly)
    #call main function of the main program:
        #1) make main program
        #2) main program takes dest
            #2.a) if a file; runs parser on file
            #2.b) if a directory: use loop that uses parser on each file
    #enter infinite loop
    #remove write_init() in Parser
    return build_assembly


def write_label(label):
    build_assembly = []
    build_assembly.append("("+label+")") #foo$L1
    return build_assembly


def write_go_to(label):
    build_assembly = []
    build_assembly.append(label)
    build_assembly.append("0;JMP")
    return build_assembly


def write_if(label):
    build_assembly = []
    build_assembly.append("@SP")
    build_assembly.append("AM=M-1")
    build_assembly.append("D=M")
    build_assembly.append(label)
    build_assembly.append("D;JGT") #unsure if they wnat zero for if-goto
    build_assembly.append("D;JLT")
    return build_assembly

def write_function(function_name, num_locals):
    build_assembly = []
    build_assembly.append("("+function_name+")")
    for x in range(0, num_locals):
        build_assembly.append("@SP") #256
        build_assembly.append("A=M") #256, M = 0
        build_assembly.append("M=0")
        _inc_sp(build_assembly)

    # if num_locals > 0:
    #     build_assembly.append("@LCL")
    #     build_assembly.append("AD=M")
    #     build_assembly.append("M=0")
    #     _inc_sp(build_assembly)
    # for x in range(0, num_locals-1):
    #     build_assembly.append("@LCL")
    #     build_assembly.append("AD=D+1")
    #     build_assembly.append("M=0")
    #     _inc_sp(build_assembly)
    return build_assembly


def write_call(function_name, num_locals):
    build_assembly = []
    return_label = function_name +"$RETURN"
    #push return address
    build_assembly.append("@"+return_label)
    build_assembly.append("D=A")
    build_assembly.append("@SP")
    build_assembly.append("A=M")
    build_assembly.append("M=D")
    _inc_sp(build_assembly)
    #push LCL
    _push_stack_segment_pointer(build_assembly, "LCL")
    _inc_sp(build_assembly)
    #push ARG
    _push_stack_segment_pointer(build_assembly, "ARG")
    _inc_sp(build_assembly)
    #push THIS
    _push_stack_segment_pointer(build_assembly, "THIS")
    _inc_sp(build_assembly)
    #push THAT
    _push_stack_segment_pointer(build_assembly, "THAT")
    _inc_sp(build_assembly)
    #ARG = SP-n-5
    build_assembly.append("@"+str(num_locals))
    build_assembly.append("D=A")
    build_assembly.append("@5")
    build_assembly.append("D=D+A")
    build_assembly.append("@SP")
    build_assembly.append("D=M-D")
    build_assembly.append("@ARG")
    build_assembly.append("M=D")
    #LCL = SP
    build_assembly.append("@SP")
    build_assembly.append("D=M")
    build_assembly.append("@LCL")
    build_assembly.append("M=D")
    #goto f
    build_assembly.append("@"+function_name)
    build_assembly.append("0;JMP")
    #(return address)
    build_assembly.append("("+return_label+")")
    return build_assembly

def write_return():
    build_assembly = []
    #R13 = FRAME, R14 = RET
    #FRAME = LCL
    build_assembly.append("@LCL")
    build_assembly.append("D=M")
    build_assembly.append("@R13")
    build_assembly.append("M=D")
    #RET = *(FRAME-5)
    build_assembly.append("@5")
    build_assembly.append("AD=D-A")
    build_assembly.append("D=M")
    build_assembly.append("@R14")
    build_assembly.append("M=D")
    #*ARG = POP()
    _pop_val_stack(build_assembly)
    build_assembly.append("@ARG")
    build_assembly.append("A=M")
    build_assembly.append("M=D")
    #SP = ARG+1
    build_assembly.append("@ARG")
    build_assembly.append("D=M+1")
    build_assembly.append("@SP")
    build_assembly.append("M=D")
    #set R15 = value of FRAME address
    build_assembly.append("@R13")
    build_assembly.append("D=M")
    build_assembly.append("@R15")
    build_assembly.append("M=D")
    #THAT = *(FRAME-1)
    build_assembly.append("@R15")
    build_assembly.append("AM=M-1")
    build_assembly.append("D=M")
    build_assembly.append("@THAT")
    build_assembly.append("M=D")
    #THIS = *(FRAME-2)
    build_assembly.append("@R15")
    build_assembly.append("AM=M-1") #315
    build_assembly.append("D=M")
    build_assembly.append("@THIS")
    build_assembly.append("M=D")
    #ARG = *(FRAME-3)
    build_assembly.append("@R15")
    build_assembly.append("AM=M-1") #314
    build_assembly.append("D=M")
    build_assembly.append("@ARG")
    build_assembly.append("M=D")
    #LCL = *(FRAME-4)
    build_assembly.append("@R15")
    build_assembly.append("AM=M-1")
    build_assembly.append("D=M")
    build_assembly.append("@LCL")
    build_assembly.append("M=D")
    #goto ret
    build_assembly.append("@R14") #R14 = 200
    build_assembly.append("A=M")
    build_assembly.append("0;JMP")
    return build_assembly



def _decide_push_segment(build_assembly, seg_strip, index, filename):
    if seg_strip == "constant":
        _add_constant(build_assembly, index)

    if seg_strip == "local":
        _push_stack(build_assembly, "LCL", index)
#untested from here
    if seg_strip == "argument":
        _push_stack(build_assembly, "ARG", index)

    if seg_strip == "this":
        _push_stack(build_assembly, "THIS", index)

    if seg_strip == "that":
        _push_stack(build_assembly, "THAT", index)

    if seg_strip == "temp":
        tmp_index = index + 5
        _push_stack_tmp(build_assembly, tmp_index)

    #undone
    if seg_strip == "pointer":
        _push_stack_pointer(build_assembly, index)

    if seg_strip == "static":
        _push_stack_static(build_assembly, index, filename)


def _decide_pop_segment(build_assembly, seg_strip, index, filename):
    if seg_strip == "local":
        _pop_register(build_assembly, "LCL", index)
#untested from here
    if seg_strip == "argument":
        _pop_register(build_assembly, "ARG", index)

    if seg_strip == "this":
        _pop_register(build_assembly, "THIS", index)

    if seg_strip == "that":
        _pop_register(build_assembly, "THAT", index)

    if seg_strip == "temp":
        tmp_index = index + 5
        _pop_register_tmp(build_assembly, tmp_index)

    if seg_strip == "pointer":
        _pop_register_pointer(build_assembly, index)

    if seg_strip == "static":
        _pop_register_static(build_assembly, index, filename)


#helper methods
def _inc_sp(build_assembly):
    build_assembly.append("@SP")
    build_assembly.append("M=M+1")  # inc SP

def _push_stack_segment_pointer(build_assembly, segment):
    build_assembly.append("@" + segment)
    build_assembly.append("D=M")
    build_assembly.append("@SP")
    build_assembly.append("A=M")
    build_assembly.append("M=D")


def _pop_top_two_of_stack(build_assembly):
    build_assembly.append("@SP")
    build_assembly.append("AM=M-1")
    build_assembly.append("D=M")
    build_assembly.append("@SP")
    build_assembly.append("AM=M-1")  # pointer goes to allocated space here


def _pop_val_stack(build_assembly):
    build_assembly.append("@SP")
    build_assembly.append("AM=M-1")
    build_assembly.append("D=M")


def _push_stack_segment(build_assembly):
    build_assembly.append("@SP")
    build_assembly.append("A=M")
    build_assembly.append("M=D")


def _initiate_pointers(build_assembly):
    #STACK
    #SP
    build_assembly.append("@256")
    build_assembly.append("D=A")
    build_assembly.append("@SP")
    build_assembly.append("M=D")
    _registers_for_testing(build_assembly)


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


#constant adder
def _add_constant(build_assembly, index):
    build_assembly.append("@" + str(index))
    build_assembly.append("D=A")  # store const in D-register
    build_assembly.append("@SP")
    build_assembly.append("A=M")  # set assembly to regiter[SP], SP Val NOT RAM_ADDRESS[0]
    build_assembly.append("M=D")  # store const in register[SP]
    _inc_sp(build_assembly)


#pop into registers
def _pop_register(build_assembly, segment, index):
    #set register to: base+index
    build_assembly.append("@"+str(index))
    build_assembly.append("D=A")
    build_assembly.append("@"+segment)
    build_assembly.append("M=M+D")
    #pop val from stack
    _pop_val_stack(build_assembly)
    #insert D-register into segment of base+index
    build_assembly.append("@"+segment)
    build_assembly.append("A=M")
    build_assembly.append("M=D")
    #reset to segment to base
    build_assembly.append("@"+str(index))
    build_assembly.append("D=A")
    build_assembly.append("@"+segment)
    build_assembly.append("M=M-D")


def _pop_register_tmp(build_assembly, tmp_index):
    _pop_val_stack(build_assembly)
    build_assembly.append("@" + str(tmp_index))
    build_assembly.append("M=D")


def _pop_register_pointer(build_assembly, pointer_index):
    _pop_val_stack(build_assembly)

    if pointer_index == 0:
        build_assembly.append("@THIS")
    else: #pointer is 1
        build_assembly.append("@THAT")
    build_assembly.append("M=D")

def _pop_register_static(build_assembly, static_index, filename):
    _pop_val_stack(build_assembly)
    build_assembly.append("@"+filename+"."+str(static_index))
    build_assembly.append("M=D")


#push register methods
def _push_stack(build_assembly, segment, index):
    build_assembly.append("@"+str(index))
    build_assembly.append("D=A")
    build_assembly.append("@"+segment)
    build_assembly.append("A=M+D")
    build_assembly.append("D=M")
    _push_stack_segment(build_assembly)
    _inc_sp(build_assembly)


def _push_stack_tmp(build_assembly, tmp_index):
    build_assembly.append("@" + str(tmp_index))
    build_assembly.append("D=M")
    _push_stack_segment(build_assembly)
    _inc_sp(build_assembly)


def _push_stack_pointer(build_assembly, pointer_index):
    if pointer_index == 0:
        build_assembly.append("@THIS")
    else: #pointer_index is 1
        build_assembly.append("@THAT")

    build_assembly.append("D=M")
    _push_stack_segment(build_assembly)
    _inc_sp(build_assembly)


def _push_stack_static(build_assembly, static_index, filename):
    build_assembly.append("@"+filename+"."+str(static_index))
    build_assembly.append("D=M")
    _push_stack_segment(build_assembly)
    _inc_sp(build_assembly)


#arithmetic bit-wise operations
def _bitwise_stack(build_assembly, bitwise_operation):
    _pop_top_two_of_stack(build_assembly)
    build_assembly.append(bitwise_operation)
    _inc_sp(build_assembly)


def _bitwise_not_stack(build_assembly):
    build_assembly.append("@SP")
    build_assembly.append("AM=M-1")
    build_assembly.append("M=!M")
    _inc_sp(build_assembly)


#arithmetic, equals operations
def _equals_stack(build_assembly, equals_generator, jmp_conditional):
    _pop_top_two_of_stack(build_assembly)
    build_assembly.append("D=M-D")
    build_assembly.append("@Loop" + str(equals_generator))
    build_assembly.append("D;"+jmp_conditional)
    build_assembly.append("@SP")
    build_assembly.append("A=M")
    build_assembly.append("M=0")
    build_assembly.append("@Loop"+str(equals_generator)+"END")
    build_assembly.append("0;JMP")
    build_assembly.append("(Loop" + str(equals_generator)+")")
    build_assembly.append("@SP")
    build_assembly.append("A=M")
    build_assembly.append("M=-1")
    build_assembly.append("(Loop"+ str(equals_generator)+"END)")
    _inc_sp(build_assembly)


#arithmetic operations
def _neg_stack(build_assembly):
    build_assembly.append("@SP")
    build_assembly.append("M=M-1")
    build_assembly.append("A=M")
    build_assembly.append("D=M")
    build_assembly.append("M=M-D")
    build_assembly.append("M=M-D")
    _inc_sp(build_assembly)


def _add_stack(build_assembly):
    build_assembly.append("@SP")
    build_assembly.append("M=M-1")
    build_assembly.append("A=M")
    build_assembly.append("D=M")
    build_assembly.append("M=0")
    build_assembly.append("@SP")
    build_assembly.append("M=M-1")
    build_assembly.append("A=M")
    build_assembly.append("M=M+D")
    _inc_sp(build_assembly)


def _sub_stack(build_assembly):
    build_assembly.append("@SP")
    build_assembly.append("M=M-1")
    build_assembly.append("A=M")
    build_assembly.append("D=M")
    build_assembly.append("M=0")
    build_assembly.append("@SP")
    build_assembly.append("M=M-1")
    build_assembly.append("A=M")
    build_assembly.append("M=M-D")
    _inc_sp(build_assembly)



#LCL = 800
#ARG = 900
#THIS = 8000
#THAT = 13000
#Pointer = 999, 1000(8000, 13000)
#TMP = 5-12