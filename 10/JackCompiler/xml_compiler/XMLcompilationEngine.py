from collections import OrderedDict
import xml.etree.cElementTree as ET

op = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
unaryOp = ["-", "~"]
term_specials = ['.', '[', '(', ')']
#ignored  "keywordConstant"
term = ["integerConstant", "stringConstant", "identifier", "keyword"]
subroutine_types = ["constructor", "function", "method"]
types = ["int", "char", "boolean"] #and classname
subroutine_return_types = [types, "void"]
statements = ["let", "if", "while", "do", "return"] #else-statement is inside if-statement?

class XMLCompilationEngine():
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.skiplist = ['<tokens>', '<?xml version="1.0" ?>', '</tokens>']
        # key = child, value = parent
        self.structure = OrderedDict()
        #skip first to lines
        self.line_counter = 2
        self.program = []
        self.CompileClass()

    def CompileClass(self):
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

            self._write_file()


    def compile_expression_list(self):
        self._create_new_node("expressionList")

        while True:
            if self.cur_text != ')':
                self.compile_expression()

            if self.cur_text == ',':
                self._transfer_line()

            if self.cur_text == ')':
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
        #while (statement) assumes ( has already been written
        elif self.cur_text in unaryOp:
            self._create_new_node("term")
            self._transfer_line()
            self._next_line_as_node()
            self.compile_term()
            self._update_structure_end()
        elif self.cur_tag == 'identifier' and text_ahead == '[':
            self._create_new_node("term")
            self.transfer_and_next(2)
            self.compile_expression()
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

        #add while for (() - 2 > 2)
        elif self.cur_tag in term:
            self._create_new_node("term")
            self._transfer_line()
            #..
            self._next_line_as_node()
            self._update_structure_end()
            #fix with (
        #if self.cur_text == ')':
        #    self._update_structure_end()

    def compile_expression(self):
        self._create_new_node("expression")

        while True:
            self.compile_term()

            if self.cur_text not in op:
                self._update_structure_end()
                break
            else:
                self._transfer_line()
            self._next_line_as_node()


    def compile_var_dec(self):
        self._create_new_node("varDec")

        while True:
            self._transfer_line()
            if self.cur_text == ';':
                self._update_structure_end()
                break
            self._next_line_as_node()

    def compile_while(self):
        self._create_new_node("whileStatement")

        while True:
            #call expression here..
            if self.cur_text == '(':
                self._transfer_line()
                self._next_line_as_node()
                self.compile_expression()

            self._transfer_line()


            if self.cur_text == '{':
                self.compile_statements()

            if self.cur_text == '}':

                self._transfer_line()
                self._update_structure_end()
                break

            self._next_line_as_node()

    def compile_if(self):
        self._create_new_node("ifStatement")
        while True:
            if self.cur_text == '{':
                self._transfer_line()
                self.compile_statements()
            elif self.cur_text == '}':
                ahead_tag, ahead_text = self._read_ahead()
                self._transfer_line()
                if ahead_text == 'else':
                    self._next_line_as_node()
                    self.transfer_and_next()
                    continue
                else:
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
        while True:
            if self.cur_text != 'do':
                self.compile_subroutine_call()

            if self.cur_text == ';':
                self._transfer_line()
                self._update_structure_end()
                break
            else:
                self._transfer_line()
                self._next_line_as_node()

    def compile_return(self):
        self._create_new_node("returnStatement")
        while True:
            if self.cur_text == ';':
                self._transfer_line()
                self._update_structure_end()
                break
            elif self.cur_text == 'return':
                self._transfer_line()
                self._next_line_as_node()
            else:
                self.compile_expression()


    def compile_let(self):
        self._create_new_node("letStatement")
        while True:
            if self.cur_text == '=' or self.cur_text == '[':
                self._transfer_line()
                self._next_line_as_node()
                self.compile_expression()

            if self.cur_text == ';':
                self._transfer_line()
                self._update_structure_end()
                break
            else:
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
        #skip (
        self._next_line_as_node()
        while True:
            if self.cur_text == ')':
                self._update_structure_end()
                break
            self._transfer_line()
            self._next_line_as_node()

    def compile_subroutine_call(self):
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
        while True:

            if self.cur_text == '(' and self.current_parent.tag == 'subroutineDec':
                self._transfer_line()
                self.compile_parameterlist() #here
            if self.cur_text == '{':
                self.compile_subroutine_body()
            if self.cur_text == '}':
                self._update_structure_end()
                break

            self._transfer_line()
            self._next_line_as_node()

    def compile_class_var_dec(self):
        self._create_new_node("classVarDec")
        while True:
            self._transfer_line()
            if self.cur_text == ';':
                self._update_structure_end()
                break
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
            # print(self.cur_result_line)
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
            print(self.cur_text)
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

