class Node:
    def __init__(self, val):
        self.__val = val
        self.__children = []

    def get_val(self):
        return self.__val

    def get_children(self):
        return self.__children

    def add_child(self, child):
        self.__children.append(child)


class ParsingTree:
    def __init__(self, root):
        self.__root = root

    def insert(self, node):
        current = self.root
        for w in node:
            flag = False
            for child in current.children:
                if child.val == w:
                    flag = True
                    current = child
                    break
            if not flag:
                new_node = TrieNode(w)
                current.children.append(new_node)
                current = new_node
        current.isWord = True
        