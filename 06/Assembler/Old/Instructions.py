#1) ■ For each field, generate the corresponding bits in the machine language.
import c_table as ins


def InstructionToBinary(instruction):
    if "@" in instruction:
        return a_instruction(instruction)
        #return split_nth_character(4, a_instruction(instruction))
    else:
        return c_instruction(instruction)
        #return split_nth_character(4, c_instruction(instruction))

def a_instruction(instruction):
    constant_val = instruction[1:]
    return '0' + '{0:015b}'.format(int(constant_val))

def c_instruction(instruction):
    MSB_3 = "111"
    #check if jump or not
    if ";" in instruction:
        return MSB_3 + c_jump(instruction)
    elif "=" in instruction:
        return MSB_3 + c_simple_comp(instruction)
    else:
        return None

def c_comp(expression):
    return ins.c_comp[expression]


def c_dest(expression):
    comp = expression.split('=')
    return ins.c_dest[comp[0]]

def c_simple_comp(instruction):
    # comp[0] = dest
    # comp[1] = comp
    comp = instruction.split('=')
    cur_comp = c_comp(comp[1])
    cur_dest = c_dest(comp[0])
    jmp = "000"
    return cur_comp+cur_dest+jmp


def c_jump(expression):
    jmp = expression.split(";")
    #[0]: A=M-D, [1]: JET...
    cur_dest = ""
    cur_comp = ""
    if "=" in jmp[0]:
        dest = jmp[0].split("=")
        cur_dest = ins.c_dest[dest[0]]
        cur_comp = c_comp(dest[1])
    else:
        cur_comp = c_comp(jmp[0])
        cur_dest = "000"

    cur_jmp = ins.c_jump[jmp[1]]
    return cur_comp + cur_dest + cur_jmp


def split_nth_character(nth_char, line):
    return [line[i:i+nth_char] for i in range(0, len(line), nth_char)]

#print(InstructionToBinary("D=D+1"))
#print(generateField("D=D+1;JEQ"))
#print(generateField("M=M+1"))
#print(generateField("@25"))

# 1) Read input file / every line
# 2) print out result
# 3) tests w/o symbols



# ?) begin symbols..
# ?) see Parser


