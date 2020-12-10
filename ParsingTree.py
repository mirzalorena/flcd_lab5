class Node:
    def __init__(self, val):
        self.__val = val
        self.children = []

    def get_val(self):
        return self.__val

    def get_children(self):
        return self.children

    def add_child(self, child):
        self.children.append(child)


class ParsingTree:
    def __init__(self, root):
        self.__root = root
        self.__current = 1

    def add_child(self, child):
        self.__root.add_child(child)

    def insert1(self, node):
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

    def search_and_insert(self, level, node, kids2):
        if self.__root == None:
            return False

        if level == self.__current - 1:
            kids = self.__root.get_children()
            for i in range (len(kids)):
                if kids[i].get_val() == node:
                    for elem in kids2:
                        kids[i].add_child(Node(elem))
                    self.__current += 1
                    return True
        else:
            kids = self.__root.get_children()
            for i in range(len(kids)):
                if self.search_and_insert(level + 1, node, kids2):
                    break

    def inorder(self, node):
        if node == None:
            return

        total = len(node.children)

        for i in range(total - 1):
            self.inorder(node.children[i])

        print(node.get_val(), " ")

        self.inorder(node.children[total - 1])

    def get_root(self):
        return self.__root

    def set_root(self, root):
        self.__root = root