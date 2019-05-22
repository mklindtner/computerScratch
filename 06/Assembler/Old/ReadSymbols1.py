import SymbolTable as st
from enum import Enum

def check_for_symbol_variables(symbol):
    if not st.contains(symbol):
        st.addEntry(symbol, st.inc_symbol_var_count())


def is_pseduo_command():
    return None


def decide_command_type(line):
    l = line.split()
    if "//" in l[0]:
        return None
    elif "@" in l[0]:
        return CommandType.A_COMMAND
    elif "(" in l[0]:
        return CommandType.L_COMMAND
    else: #better check here
        return CommandType.C_COMMAND


def read_file(file):
    instruction_address = 0
    with open(file, "r") as f:
        for line in f:
            cur_type = decide_command_type(line)
            if cur_type == CommandType.A_COMMAND:
                instruction_address += 1

            if cur_type == CommandType.C_COMMAND:
                instruction_address += 1

            if cur_type == CommandType.L_COMMAND:
                #cut string into varaible w/o '(' & ')' i.e. (LOOP) = LOOP
                var_name = ''.join(line)
                st.addEntry(var_name[1:-2], instruction_address)
        print(st.hold_symbols.symbol_table)


class CommandType(Enum):
    A_COMMAND = 1,
    C_COMMAND = 2,
    L_COMMAND = 3


#read_file(os.sys.argv[1])
read_file("assm_file2.asm")

#use switcher..
