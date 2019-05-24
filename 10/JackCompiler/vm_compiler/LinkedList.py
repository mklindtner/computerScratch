class Node:
    def __init__(self, dataval=None):
        self.dataval = dataval
        self.nextval = None


class ReversedLinkedList():
    def __init__(self, head):
        self.head = Node(head)
        self.cur_node = Node(head)

    def add_node(self, cur_dict):
        node = Node(cur_dict)
        node.nextval = self.cur_node #go backwards
        self.cur_node = node
        return node

    def next(self):
        self.cur_node = self.cur_node.nextval
        return self.cur_node


#d_1 = {'name': 'i', 'type':'int', 'kind':'field', "#":'2'}
#d_2 = {'b': 'totally'}
#d_3 = {'ok':'hej'}


#LL = ReversedLinkedList(d_1)
#LL.add_node(d_2)
#LL.add_node(d_3)
#print(LL.next().dataval)
#print(LL.next().dataval)

