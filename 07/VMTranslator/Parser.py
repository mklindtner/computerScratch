from CoderWriter import write_arithmetic, write_push_pop, write_init, write_label, write_go_to, write_if, write_call, write_function, write_return
from CommandType import CommandType
import os

class Parser:
    is_debug = True
    def __init__(self, file):
        self.file = file
        self.write_file = ""
        self.vm_hack = []
        self.jump_tracker = 0
        self.vm_debug = []

    def read_file(self):
        hest = []
        with open(self.file) as f:
            line_number = 0
            for line in f:
                expr = self._delete_comments_whitespace(line)
                if not expr:
                    continue
                cmd_type = self._command_type(expr[0])

                path, file_ext = os.path.splitext(self.file)
                filename = os.path.basename(path)
                self.vm_hack.append(self._write_line_to_hack(cmd_type, expr, filename))

                hest = self._write_line_to_hack(cmd_type, expr, filename)
                for h in hest:
                    line_number += 1
                    self.vm_debug.append(line_number)
                    self.vm_debug.append(h)
            res = (self.vm_hack, self.vm_debug)
            return res

    def _auth_write_asm_ext(self, filename, file_ext):
        if file_ext.strip() == ".vm": #here check this
            return filename + ".asm"
        return None # throw error

    def _write_line_to_hack(self, cmd_type, expr, filename):
        # command_type:push, arg1:constnat , arg2:3
        is_debug = True
        if cmd_type is CommandType.C_PUSH or cmd_type is CommandType.C_POP:
            return write_push_pop(cmd_type, self.arg1(cmd_type, expr), self.arg2(expr), filename)
        elif cmd_type is CommandType.C_ARITMETHIC:
            self.jump_tracker += 1
            return write_arithmetic(self.arg1(cmd_type, expr), self.jump_tracker)
        elif cmd_type is CommandType.C_LABEL:
            label_name = expr[1]
            label = filename + "$" + label_name
            return write_label(label)
        elif cmd_type is CommandType.C_GOTO:
            label_name = expr[1]
            label = "@" + filename + "$" + label_name
            return write_go_to(label)
        elif cmd_type is CommandType.C_IF:
            label_name = expr[1]
            label = "@" + filename + "$" + label_name
            return write_if(label)
        elif cmd_type is CommandType.C_FUNCTION:
            func_name = expr[1]
            return write_function(func_name, self.arg2(expr))
        elif cmd_type is CommandType.C_RETURN:
            return write_return()
        elif cmd_type is CommandType.C_CALL:
            locals_val = str(expr[2])
            func_name = expr[1]
            return write_call(func_name, locals_val)

    def _delete_comments_whitespace(self, line):
            if "//" in line:
                index_of_comment = line.index("//")
                return line[0:index_of_comment].split()
            else:
                return line.split()

    #line.split[0]
    def _command_type(self, word):
        return {
            "pop": CommandType.C_POP,
            "push": CommandType.C_PUSH,
            #arithmetic
            "add": CommandType.C_ARITMETHIC,
            "sub": CommandType.C_ARITMETHIC,
            "neg": CommandType.C_ARITMETHIC,
            #equals
            "eq": CommandType.C_ARITMETHIC,
            "lt": CommandType.C_ARITMETHIC,
            "gt": CommandType.C_ARITMETHIC,
            #bitwise
            "not": CommandType.C_ARITMETHIC,
            "and": CommandType.C_ARITMETHIC,
            "or": CommandType.C_ARITMETHIC,
            #flow of control
            "goto": CommandType.C_GOTO,
            "if-goto": CommandType.C_IF,
            "label": CommandType.C_LABEL,
            #func, return, call
            "function": CommandType.C_FUNCTION,
            "return": CommandType.C_RETURN,
            "call": CommandType.C_CALL
        }[word]

    def arg1(self, cmd_type, line):
        if cmd_type is CommandType.C_RETURN:
            return
        elif cmd_type is CommandType.C_ARITMETHIC or cmd_type is CommandType.C_IF:
            return line[0]
        else:
            return line[1] #push local 1: local

    #C_PUSH, C_POP, C_FUNCTION, C_CALL
    def arg2(self, line):
        return int(line[2])

