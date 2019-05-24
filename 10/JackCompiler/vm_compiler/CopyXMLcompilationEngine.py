from collections import OrderedDict
import xml.etree.cElementTree as ET
from vm_compiler import SymbolTable, VMWriter

op = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
unaryOp = ["-", "~"]
term_specials = ['.', '[', '(', ')']
#ignored  "keywordConstant"
term = ["integerConstant", "stringConstant", "identifier", "keyword"]
subroutine_types = ["constructor", "function", "method"]
types = ["int", "char", "boolean"] #and classname
subroutine_return_types = [types, "void"]
statements = ["let", "if", "while", "do", "return"] #else-statement is inside if-statement?

class CompilationEngine():
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.skiplist = ['<tokens>', '<?xml version="1.0" ?>', '</tokens>']
        # key = child, value = parent
        self.structure = OrderedDict()
        #skip first to lines
        self.line_counter = 2
        self.program = []
        self.SymbolTable = SymbolTable.SymbolTable()
        self.VMWriter = VMWriter.VMWriter(output)
        self.cur_subroutine_name = ""
        self.cur_subroutine_type = " "
        self.cur_subroutine_prev_name = None
        self.label_counter_while = 0
        self.label_counter_if = 0
        self.is_constructor = False
        self.compile_class()
        self.VMWriter.close()

    def compile_class(self):
        with open(self.input) as file:
            for line in file:
                self.program.append(line)
            while True:
                self._next_line_as_node()
                if self.cur_text == "class":
                    self.tree = ET.Element(self.cur_text)
                    # add first token under class
                    self._transfer_line(True)
                    #root has no parent
                    self.structure.update({self.tree: None})
                    self.current_parent = self.tree

                elif self.cur_text == "field" or self.cur_text == "static":
                    self.compile_class_var_dec()

                elif self.cur_text in subroutine_types:
                    self.compile_subroutine_dec()

                elif (self.cur_text == "}"):
                    self._transfer_line()
                    break

                else:
                    self._transfer_line()
                    if self.current_parent.tag == 'class' and self.cur_tag == 'identifier':
                        #category, defined, kind
                        self._create_identifier_info("class", "true", "this")
                        self.class_name = self.cur_text
            self._write_file()

    def compile_expression_list(self):
        self._create_new_node("expressionList")
        n_args = 0
        #push_object = True
        #push_this = True
        push_pointer = True
        run_once = True
        while True:
            if self.cur_text != ')':
                n_args += 1
                if run_once:
                    if self.cur_subroutine_type.strip() == 'method' and push_pointer:
                        if self.cur_subroutine_prev_name:
                            self._vm_write_sub_prevname()
                        else:
                            push_pointer = False
                            self.VMWriter.write_push("pointer", 0)
                    run_once = False
                self.compile_expression()

            if self.cur_text == ',':
                self._transfer_line()

            if self.cur_text == ')':
                #VM
                pushed_pointer = False
                self.cur_n_args = n_args

                #edge case of empty () and method
                if self.cur_n_args == 0 and self.cur_subroutine_type.strip() == 'method':
                    #case where: method.run()...
                    if self.cur_subroutine_prev_name is not None:
                       self._vm_write_sub_prevname()
                    else:
                        self.VMWriter.write_push("pointer",0)

                #is method or function but not private method
                if "." in self.cur_subroutine_name:
                    if self.cur_subroutine_type == 'method':
                        self.cur_n_args += 1 #+1 error?
                    self.VMWriter.write_call(self.cur_subroutine_name, str(self.cur_n_args))
                else:
                    #if not pushed_pointer:
                    #    self.VMWriter.write_push("pointer", 0)
                    #pointer used to be here
                    self.cur_n_args += 1
                    self.VMWriter.write_call(self.class_name + "." + self.cur_subroutine_name.strip(), str(self.cur_n_args))

                #XML
                self._update_structure_end()
                break
            self._next_line_as_node()

    def compile_term(self):
        tag_ahead, text_ahead = self._read_ahead()

        #metod.call()
        if self.cur_tag == 'identifier' and text_ahead == '.':
            self._create_new_node("term")
            self.compile_subroutine_call()
            self._update_structure_end()
        #-x
        elif self.cur_text in unaryOp:
            coper = self.cur_text
            self._create_new_node("term")
            self._transfer_line()
            self._next_line_as_node()
            self.compile_term()

            #self.cur_text is now changed, use previous val
            unary_operator = self._operator_name_text(coper)
            self.VMWriter.write_arithmetic(unary_operator)

            self._update_structure_end()
        #array[]
        elif self.cur_tag == 'identifier' and text_ahead == '[':
            #VM
            idx = self.SymbolTable.index_of(self.cur_text)
            kind = self.SymbolTable.kind_of(self.cur_text)
            #XML
            self._create_new_node("term")
            self.transfer_and_next(2)
            self.compile_expression()
            #VM
            if kind == 'var':
                self.VMWriter.write_push("local", idx)
            elif kind == 'field': #maaybe?
                self.VMWriter.write_push("this", idx)

            self.VMWriter.write_arithmetic("add")
            self.VMWriter.write_pop("pointer", 1)
            #self.VMWriter.write_push("that", idx)
            self.VMWriter.write_push("that", 0)
            #XML
            self.transfer_and_next()
            self._update_structure_end()

        #( expression )
        elif self.cur_text == '(' or self.cur_text == ')':
            self._create_new_node("term")

            if self.cur_text == '(':
                self.transfer_and_next()
                self.compile_expression()
            if self.cur_text == ')':
                self._transfer_line()
                self._update_structure_end()
                self._next_line_as_node()

        #(() - 2 > 2)
        elif self.cur_tag in term:
            #xml
            self._create_new_node("term")
            self._transfer_line()
            #vm
            if self.cur_tag == 'identifier':
                idx = self.SymbolTable.index_of(self.cur_text)
                kind = self.SymbolTable.kind_of(self.cur_text)
                if kind == 'var':
                    self.VMWriter.write_push("local", idx)
                elif kind == "field":
                    self.VMWriter.write_push("this", idx)
                #elif kind == "argument":
                    #self.VMWriter.write_push("argument", idx)
                else:
                    self.VMWriter.write_push(kind, idx)
            elif self.cur_tag == 'stringConstant':
                self.VMWriter.write_push("constant", len(self.cur_text))
                self.VMWriter.write_call("String.new", 1)
                for s in self.cur_text:
                    self.VMWriter.write_push("constant", ord(s))
                    self.VMWriter.write_call("String.appendChar", 2)

            else:
                if self.cur_text == 'true' and self.cur_tag == 'keyword':
                    self.VMWriter.write_push("constant", 0)
                    self.VMWriter.write_arithmetic("not") #made it to here
                elif self.cur_text == 'false' and self.cur_tag == 'keyword':
                    self.VMWriter.write_push("constant", 0)
                elif self.cur_text == 'this':
                    self.VMWriter.write_push("pointer", 0)
                elif self.cur_text == 'null':
                    self.VMWriter.write_push("constant", 0)
                else:
                    self.VMWriter.write_push("constant", self.cur_text)
            #xml
            self._next_line_as_node()
            self._update_structure_end()

    def compile_expression(self):
        self._create_new_node("expression")
        op_list = []
        while True:
            self.compile_term()
            if self.cur_text not in op:
                for symbol in op_list:
                    if symbol == 'mult':
                        self.VMWriter.write_call("Math.multiply", "2")
                    elif symbol == 'div':
                        self.VMWriter.write_call("Math.divide", "2")
                    else:
                        self.VMWriter.write_arithmetic(symbol)
                self._update_structure_end()
                break
            #write in +,- etc. operators
            else:
                #XML
                self._transfer_line()
                #VM
                op_list.append((self._operator_name_text(self.cur_text, True)))
            self._next_line_as_node()

    def compile_var_dec(self):
        self._create_new_node("varDec")
        var_type = " "
        CATEGORY = "var"
        while True:
            self._transfer_line()
            if self.cur_text == ';':
                self._update_structure_end()
                break
            if self.cur_tag == 'keyword':
                if self.cur_text != "var":
                    var_type = self.cur_text
            if self.cur_tag == 'identifier':
                if var_type.isspace():
                    var_type = self.cur_text
                else:
                    self._create_identifier_info(CATEGORY, "true", var_type)
                    self.SymbolTable.define(self.cur_text, var_type, CATEGORY)
            self._next_line_as_node()

    def compile_while(self):
        self._create_new_node("whileStatement")
        cur_counter = self.label_counter_while
        while True:
            if self.cur_text == '(':
                #VM
                self.VMWriter.write_label("WHILE_EXP"+str(cur_counter))
                self.label_counter_while += 1
                #XML
                self._transfer_line()
                self._next_line_as_node()
                self.compile_expression()
            self._transfer_line()
            if self.cur_text == '{':
                #VM

                self.VMWriter.write_arithmetic("not")
                self.VMWriter.write_if_goto("WHILE_END" + str(cur_counter))
                #XML
                self.compile_statements()
            if self.cur_text == '}':
                #VM
                self.VMWriter.write_goto("WHILE_EXP"+str(cur_counter))
                self.VMWriter.write_label("WHILE_END" + str(cur_counter))

                #XML
                self._transfer_line()
                self._update_structure_end()
                break

            self._next_line_as_node()

    def compile_if(self):
        self._create_new_node("ifStatement")
        if_counter = str(self.label_counter_if)
        self.label_counter_if += 1
        contains_else = False
        prev_else = " "
        while True:
            if self.cur_text == '{':
                #VM
                if prev_else == 'else':
                    prev_else = " "
                else:
                    #print("-----A-----"+if_counter)
                    self.VMWriter.write_if_goto("IF_TRUE_AA"+if_counter)
                    self.VMWriter.write_goto("IF_FALSE_AA"+if_counter)
                    self.VMWriter.write_label("IF_TRUE_AA"+if_counter)
                self._transfer_line()
                self.compile_statements()

            elif self.cur_text == '}':
                #VM
                #contains_else = False
                ahead_tag, ahead_text = self._read_ahead()
                self._transfer_line()
                if ahead_text == 'else':
                    contains_else = True
                    #VM
                    #print("----B----" + if_counter)
                    self.VMWriter.write_goto("IF_END_AA"+if_counter)
                    self.VMWriter.write_label("IF_FALSE_AA"+if_counter)
                    #VM/XML
                    self.compile_statements()
                    #XML
                    self._next_line_as_node()
                    prev_else = self.cur_text
                    self.transfer_and_next()
                    continue
                else:
                    if contains_else:
                        self.VMWriter.write_label("IF_END_AA"+if_counter)
                        #print("----C----"+if_counter)
                    else:
                        self.VMWriter.write_label("IF_FALSE_AA"+if_counter)
                        #print("----D----"+if_counter)

                    self._update_structure_end()
                    break
            elif self.cur_text == '(':
                self._transfer_line()
                self._next_line_as_node()
                self.compile_expression()
            else:
                self._transfer_line()
                self._next_line_as_node()

    def compile_do(self):
        self._create_new_node("doStatement")
        self.cur_subroutine_name = ""
        self.cur_subroutine_prev_name = None
        while True:
            if self.cur_text != 'do':
                self.compile_subroutine_call()

            if self.cur_text == ';':
                #test

                #xml
                self._transfer_line()
                self._update_structure_end()
                #vm
                self.VMWriter.write_pop("temp", "0")
                break
            else:
                self._transfer_line()
                self._next_line_as_node()

    def compile_return(self):
        self._create_new_node("returnStatement")
        is_void = True
        while True:
            if self.cur_text == ';':
                #XML
                self._transfer_line()
                self._update_structure_end()
                #VM
                if is_void:
                    self.VMWriter.write_push("constant", "0")
                self.VMWriter.write_return()

                break
            elif self.cur_text == 'return':
                self._transfer_line()
                self._next_line_as_node()
            else:
                is_void = False
                self.compile_expression()

    def compile_let(self):
        self._create_new_node("letStatement")
        cur_let_name = " "
        is_array = False
        while True:
            if self.cur_text == '=' or self.cur_text == '[':
                #XML
                self._transfer_line()
                self._next_line_as_node()
                self.compile_expression()

            if self.cur_text == ';':
                #XML
                self._transfer_line()
                self._update_structure_end()
                #VM
                idx = self.SymbolTable.index_of(cur_let_name)
                segment = self.SymbolTable.kind_of(cur_let_name)
                if is_array:
                    # assign That and push contrived value to base of THAT
                    self.VMWriter.write_pop("temp", 0)
                    self.VMWriter.write_pop("pointer", 1)
                    self.VMWriter.write_push("temp", 0)
                    self.VMWriter.write_pop("that", 0)
                    is_array = False
                #want to write to attribute
                elif segment == "var":
                    self.VMWriter.write_pop("local", idx)
                elif segment == 'field':
                    self.VMWriter.write_pop("this", idx)
                else:
                    self.VMWriter.write_pop(segment, idx)
                break
            else:
                if self.cur_tag == 'identifier':
                    cur_let_name = self.cur_text
                 #VM
                if self.cur_text == ']':
                    #assumes lookup vaue has been handled
                    idx = self.SymbolTable.index_of(cur_let_name)
                    kind = self.SymbolTable.kind_of(cur_let_name)
                    if kind == 'argument':
                        self.VMWriter.write_push(kind, idx)
                    else:
                        self.VMWriter.write_push("local", idx)
                    self.VMWriter.write_arithmetic("add")
                    is_array = True

                #XML
                self._transfer_line()
                self._next_line_as_node()


    def compile_statements(self):
        self._create_new_node("statements")
        while True:
            if self.cur_text == '}':
                self._update_structure_end()
                break
            if self.cur_text == 'let':
                self.compile_let()
            elif self.cur_text == 'return':
                self.compile_return()
            elif self.cur_text == 'do':
                self.compile_do()
            elif self.cur_text == 'if':
                self.compile_if()
            elif self.cur_text == 'while':
                self.compile_while()
            else:
                if self.cur_text != '{':
                    self._transfer_line()
            self._next_line_as_node()

    def compile_parameterlist(self):
        self._create_new_node("parameterList")
        self._next_line_as_node()
        tmp_name = " "
        tmp_type = " "

        while True:
            if self.cur_text == ')':
                #get last parameter
                if not tmp_name.isspace():
                    self.SymbolTable.define(tmp_name, tmp_type, "argument")
                    #self.SymbolTable._print_symbol_table_all()
                self._update_structure_end()
                break
            elif self.cur_text == ',':
                self.SymbolTable.define(tmp_name, tmp_type, "argument")
                tmp_type = " "
                tmp_name = " "
            elif tmp_type.isspace():
                tmp_type = self.cur_text
            elif tmp_name.isspace():
                tmp_name = self.cur_text

            self._transfer_line()
            self._next_line_as_node()

    def compile_subroutine_call(self):
        self.cur_subroutine_name = " "
        self.cur_subroutine_type = "method " #default presumption
        type_name = None
        while True:
            if self.cur_text == '(':
                self._transfer_line()
                self._next_line_as_node()
                self.compile_expression_list()

            if self.cur_text == ')':
                self._transfer_line()
                self._next_line_as_node()
                break
            else:
                if self.cur_text == '.':
                    #check if suborutine is a variable
                    type_name = self.SymbolTable.type_of(self.cur_subroutine_name.strip())
                    #subroutine name is a var
                    if type_name is not None:
                        self.cur_subroutine_prev_name = self.cur_subroutine_name.strip()
                        self.cur_subroutine_type = "method"
                        self.cur_subroutine_name = type_name
                    #is function
                    else:
                        self.cur_subroutine_type = "function"
                        self.cur_subroutine_prev_name = self.cur_subroutine_name.strip()

                #is method or function
                self.cur_subroutine_name += self.cur_text

                self._transfer_line()
                self._next_line_as_node()

    def compile_subroutine_body(self):
        self._create_new_node("subroutineBody")
        skip_transfer = False
        while True:
            if not skip_transfer:
                self._transfer_line()
                skip_transfer = False
            self._next_line_as_node()

            if self.cur_text in statements:
                kind_amount = self.SymbolTable.var_count("var")
                function_name = "function " + self.class_name + "." + self.cur_func_name
                self.VMWriter.write_function(function_name, kind_amount)

                if self.is_constructor:
                    self.is_constructor = False
                    push_class_var = self.SymbolTable.var_count("field")
                    self.VMWriter.write_push("constant", push_class_var)
                    self.VMWriter.write_call("Memory.alloc", 1)  # take newest index from stack
                    self.VMWriter.write_pop("pointer", 0)
                elif self.cur_subroutine_type.strip() == "method" or self.cur_sub_decl.strip() == 'method':
                    self.VMWriter.write_push("argument", 0)
                    self.VMWriter.write_pop("pointer", 0)

                self.compile_statements()

            if self.cur_text == 'var':
                self.compile_var_dec()
                skip_transfer = True

            if self.cur_text == '}':
                self._transfer_line()
                self._update_structure_end()
                break


        #add more here...

    def compile_subroutine_dec(self):
        self._create_new_node("subroutineDec")
        self.SymbolTable.start_subroutine()

        if self.cur_text == 'method':
            self.SymbolTable.define("this", self.class_name, "argument")
        tmp_type = " "
        keywords = 0
        self.cur_sub_decl = " "
        while True:
            if self.cur_tag == 'identifier' or self.cur_tag == "keyword":
                if self.cur_sub_decl.isspace():
                    self.cur_sub_decl = self.cur_text
                keywords += 1
                if tmp_type.isspace() or keywords == 2:
                    tmp_type = self.cur_text
                else:
                    self.cur_func_name = self.cur_text

            if self.cur_text == 'constructor' and self.cur_tag == 'keyword':
                self.is_constructor = True
                self.SymbolTable.start_subroutine()

            if self.cur_text == '(' and self.current_parent.tag == 'subroutineDec':
                self._transfer_line()
                self.compile_parameterlist()
            if self.cur_text == '{':
                self.compile_subroutine_body()
            if self.cur_text == '}':
                self._update_structure_end()
                break

            self._transfer_line()
            self._next_line_as_node()

    def compile_class_var_dec(self):
        self._create_new_node("classVarDec")
        var_type = " "; var_decl = ""

        while True:
            self._transfer_line()

            if self.cur_text == ';':
                self._update_structure_end()
                break

            if self.cur_tag == 'keyword':
                if self.cur_text == 'static':
                    var_decl = self.cur_text
                elif self.cur_text == 'field':
                    var_decl = self.cur_text
                else:
                    var_type = self.cur_text
            if self.cur_tag == 'identifier':
                if var_type.isspace():
                    var_type = self.cur_text
                else:
                    self._create_identifier_info(var_decl, "true", var_type)
                    self.SymbolTable.define(self.cur_text, var_type, var_decl)

            self._next_line_as_node()


    def transfer_and_next(self, times=1):
        for x in range(0, times):
            self._transfer_line()
            self._next_line_as_node()

    def _print_node(self, node):
        print(str(node.tag) + ":" + str(node.text))

    def _next_line_as_node(self):
        self.cur_result_line = self.program[self.line_counter]

        if self.cur_result_line.strip() not in self.skiplist:
            line_xml = ET.fromstring(self.cur_result_line.strip())
            self.cur_tag, self.cur_text = line_xml.tag, line_xml.text
            self.line_counter += 1

    def _read_ahead(self):
        read_ahead = self.line_counter
        next_token = self.program[read_ahead]

        if next_token.strip() not in self.skiplist:
            line_xml = ET.fromstring(next_token.strip())
            return line_xml.tag, line_xml.text

    def _transfer_line(self, is_root_node=False):
        if not is_root_node:
            cur_token = ET.SubElement(self.current_parent, self.cur_tag)
            cur_token.text = self.cur_text
        else:
            cur_token = ET.SubElement(self.tree, self.cur_tag)
            cur_token.text = self.cur_text

    def _create_new_node(self, new_node_name):
        token_indent = ET.SubElement(self.current_parent, new_node_name)
        self.structure.update({token_indent: self.current_parent})
        self.current_parent = token_indent

    def _update_structure_end(self):
        child = next(reversed(self.structure))
        parent = next(reversed(self.structure.values()))
        self.current_parent = parent
        del self.structure[child]

    def _write_file(self):
        tree_as_string = ET.tostring(self.tree, encoding="unicode", short_empty_elements=False)
        openfile = open(self.output, "w")
        openfile.write(tree_as_string)

    def _create_identifier_info(self, category, defined, kind):
        self._create_new_node("id-info")
        c = ET.SubElement(self.current_parent, "category")
        c.text = category
        d = ET.SubElement(self.current_parent, "defined")
        d.text = defined
        k = ET.SubElement(self.current_parent, "kind")
        k.text = kind
        self._update_structure_end()


    def _operator_name_text(self, symbol, is_infix=False):
        if symbol == '+':
            return "add"
        elif symbol == '*':
            return "mult"
        elif symbol == '>':
            return "gt"
        elif symbol == '<':
            return "lt"
        elif symbol == '-' and is_infix is False:
            return "neg"
        elif symbol == '-' and is_infix is True:
            return "sub"
        elif symbol == '=': #and is_infix is True:
            return "eq"
        #This is true Mikkel claims, not yet tested ..
        #elif symbol == '=' and is_infix is False:
            #return "eq_assignment"
        #--
        elif symbol == '&':
            return "and"
        elif symbol == '|':
            return "or"
        elif symbol == '~':
            return "not"
        elif symbol == '/':
            return "div"


    def _vm_write_sub_prevname(self):
        idx = self.SymbolTable.index_of(self.cur_subroutine_prev_name)
        kind = self.SymbolTable.kind_of(self.cur_subroutine_prev_name)
        if kind == "field":
            self.VMWriter.write_push("this", idx)
        else:
            self.VMWriter.write_push("local", idx)  # original: this


