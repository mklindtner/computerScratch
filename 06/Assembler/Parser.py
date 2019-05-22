from enum import Enum
import Code
import SymbolTable
import os


def initializer(file):
    program = []

    first_phase(file)
    second_phase(file, program)
    file_write = _change_ext_to_hack(file)
    with open(file_write, "w") as fw:
        for line in program:
            fw.write(line + "\n")
    return program


def first_phase(file):
    line_count = 0
    with open(file) as f:
        for line in f:
            expr = delete_comments(line)
            cmd_type = command_type(expr.split())
            if cmd_type is CommandType.L_COMMAND:
                symbol_phase1(expr.strip(), line_count)
            else:
                line_count += 1
                continue

#need to fix Loop
def second_phase(file, program):
    variable_counter = 16
    with open(file) as f:
        for line in f:
            expr = delete_comments(line)
            cmd_type = command_type(expr.split())
            if cmd_type is CommandType.A_COMMAND:
                program.append(symbol_phase2(expr.strip(), variable_counter))
            if cmd_type is CommandType.C_COMMAND:
                program.append(c_mnemonic_to_binary(expr))

def delete_comments(line):
    if "//" in line:
        index_of_comment = line.index("//")
        return line[0:index_of_comment]
    else:
        return line
    return new_line


def c_mnemonic_to_binary(expr):
    full_expression = expr.strip()
    msb_3 = "111"
    return msb_3 + _c_instruction(full_expression)

def symbol_phase2(expression, variable_counter):
    if "@" in expression:
        sym = expression[1:]
        if sym.isdigit():
            return '0' + '{0:015b}'.format(int(sym))
        if SymbolTable.contains(sym):
            return '0' + '{0:015b}'.format(int(SymbolTable.getAddress(sym)))
        else:
            SymbolTable.addEntry(sym, variable_counter)
            variable_counter += 1
            return '0' + '{0:015b}'.format(int(SymbolTable.getAddress(sym)))


def symbol_phase1(expression, line_count):
    if "(" in expression:
        SymbolTable.addEntry(expression[1:-1], line_count)
        return SymbolTable.getAddress(expression[1:-1])

#refactor "=" with stragegy pattern
def _c_instruction(expression):
    if ";" in expression:
        split_expression = expression.split(";") # ["D=A", "GTE"]
        return _c_has_jump(split_expression)
    elif "=" in expression:
        return _c_no_jump(expression)
    else:
        return _c_no_jump_no_dest(expression)


#can make class and use stragegy pattern instead
def _c_has_jump(dest_comp_jump):
    if "=" in dest_comp_jump[0]:
        dest_comp = dest_comp_jump[0].split("=")
        dest = Code.c_dest_binary(dest_mnemonic(dest_comp[0]))
        comp = Code.c_comp_binary(comp_mnemonic(dest_comp[1]))
    else: #no dest in jump scenario
        dest = Code.c_dest_binary("null")
        comp = Code.c_comp_binary(dest_comp_jump[0])

    jump = Code.c_jump_binary(dest_comp_jump[1])
    return comp + dest + jump


def _c_no_jump(dest_comp):
    return Code.c_comp_binary(comp_mnemonic(dest_comp)) + Code.c_dest_binary(dest_mnemonic(dest_comp)) + Code.c_jump_binary("null")


def _c_no_jump_no_dest(comp):
    return Code.c_comp_binary(comp) + Code.c_dest_binary("null") + Code.c_jump_binary("null")


def dest_mnemonic(dest_comp):
    return ''.join(dest_comp[0].split("="))


def comp_mnemonic(dest_comp):
    return str(dest_comp.split("=")[1])


def jump_mnemonic(destComp_jump):
    return destComp_jump[1].split(";")


def command_type(line):
    if "@" in line[0]:
        return CommandType.A_COMMAND
    if "(" in line[0]:
        return CommandType.L_COMMAND
    else: #better check here
        return CommandType.C_COMMAND

class CommandType(Enum):
    A_COMMAND = 1,
    C_COMMAND = 2,
    L_COMMAND = 3

def _change_ext_to_hack(file):
    filename, file_ext = os.path.splitext(file)
    return filename + ".hack"


initializer("Max.asm")
#initializer(os.sys.argv[1])
