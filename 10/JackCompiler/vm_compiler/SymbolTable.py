from vm_compiler import LinkedList


class SymbolTable():

    def __init__(self):
        self.class_table = {}
        self.subroutine_table = {}
        self.linked_list = LinkedList.ReversedLinkedList(self.class_table)


    def start_subroutine(self):
        self.subroutine_table = {}
        self.linked_list.add_node(self.subroutine_table)

    def define(self, name, type, kind):
        if kind == "field" or kind == 'static':
            self._save_value(name, type, kind, self.class_table)
        # ARG, VAR
        else:
            self._save_value(name, type, kind, self.subroutine_table)

    def var_count(self, kind):
        return self._find_by_criteria(key="kind",criteria=kind, return_amount=True)

    def kind_of(self, name):
        return self._find_by_criteria(key='name', criteria=name, index="kind")

    def type_of(self, name):
        return self._find_by_criteria(key='name', criteria=name, index="type")

    def index_of(self, name):
        return self._find_by_criteria(key='name', criteria=name, index="#")

    def _save_value(self, name, type, kind, cur_hashtable):
         index = 0
         for v in cur_hashtable.values():
             if v['kind'] == kind:
                 index += 1
         cur_hashtable[name] = {'name': name, 'type': type, 'kind': kind, '#': index}

    # def _find_by_criteria(self, key, criteria, index=None, return_amount=False):
    #     kind_amount = 0
    #     tmp_node = self.linked_list.cur_node
    #     while True:
    #         for k,v in tmp_node.dataval.items():
    #             if v[key] == criteria:
    #                 if return_amount:
    #                     kind_amount += 1
    #                 else:
    #                     return v[index]
    #          #if everything is destroyed .. this is the reason, THANKS DAD!
    #         if tmp_node.nextval == None:
    #             if return_amount:
    #                 return kind_amount
    #             return None
    #         tmp_node = tmp_node.nextval

    def _find_by_criteria(self, key, criteria, index=None, return_amount=False):
        kind_amount = 0
        while True:
            for k, v in self.subroutine_table.items():
                if v[key] == criteria:
                    if return_amount:
                        kind_amount += 1
                    else:
                        return v[index]

            for k, v in self.class_table.items():
                if v[key] == criteria:
                    if return_amount:
                        kind_amount += 1
                    else:
                        return v[index]

            if return_amount:
                return kind_amount
            return

    def _print_symbol_table_current(self):
        print("--SYMBOL TABLE --")
        for k,v in self.class_table.items():
            print(str(k) + ":" + str(v))
        print("----suroutine-symbol-table----")
        for k, v in self.subroutine_table.items():
            print(str(k) + ":" + str(v))

    def _print_symbol_table_all(self):
        print("----suroutine-symbol----")
        for k, v in self.subroutine_table.items():
            print(str(k) + ":" + str(v))
        print("---")
        tmp_node = self.linked_list.cur_node
        while True:
            for k, v in tmp_node.dataval.items():
                print(str(k) + ":" + str(v))
            if tmp_node.nextval == None:
                return
            tmp_node = tmp_node.nextval
            print("----NEXT Subroutine----")



#s_t = SymbolTable()

#s_t.define("l", "int", "field")
#s_t.define("i", "int", "field")
#s_t.define("j", "int", "static")
#s_t.start_subroutine()

#s_t.define("this", "main", "argument")
#s_t.define("z", "int", "var")
#s_t.define("k", "int", "var")
#s_t.define("kk", "int", "var")
#s_t.start_subroutine()

#s_t.define("q", "int", "var")
#s_t.define("ll", "int", "var")
#s_t.define("lll", "int", "var")


#s_t._print_symbol_table()
#print(s_t.var_count("argument"))
#print(s_t.kind_of("q"))
#print(s_t.index_of("lll"))
#print(s_t.type_of("z"))