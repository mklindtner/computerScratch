import c_table
#returns the mnemoic value as binary for C-instruction

def c_dest_binary(dest_mnemonic):
    return c_table.c_dest[dest_mnemonic]

def c_comp_binary(comp_mnemonic):
    return c_table.c_comp[comp_mnemonic]

def c_jump_binary(jump_mnemonic):
    return c_table.c_jump[jump_mnemonic]