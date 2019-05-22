class holdSymbols():
    def __init__(self):
        #self.symbol_variable_count = 16
        self.symbol_table = {}


hold_symbols = holdSymbols()


def constructor():
    return holdSymbols


def addEntry(symbol, address):
    hold_symbols.symbol_table[symbol] = address


def contains(symbol):
    if symbol in hold_symbols.symbol_table.keys():
        return True
    return False


def getAddress(symbol):
    return hold_symbols.symbol_table[symbol]


def inc_symbol_var_count():
    hold_symbols.symbol_variable_count  += 1


def _predefined_symbols():
    addEntry("SP", 0), addEntry("LCL", 1) ,addEntry("ARG", 2)
    addEntry("THIS", 3), addEntry("THAT", 4), addEntry("R0", 0)
    addEntry("R1", 1), addEntry("R2", 2), addEntry("R3", 3)
    addEntry("R4", 4), addEntry("R5", 5), addEntry("R6", 6)
    addEntry("R7", 7),addEntry("R8", 8), addEntry("R9", 9)
    addEntry("R10", 10), addEntry("R11", 11),addEntry("R12", 12)
    addEntry("R13", 13) ,addEntry("R14", 14) ,addEntry("R15", 15)
    addEntry("SCREEN", 16384), addEntry("KBD", 24576)


def show_symbols():
    for key,val in hold_symbols.symbol_table.items():
        print("key:" + key, "\tval:" + str(val))

_predefined_symbols()



