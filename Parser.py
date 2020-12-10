from Grammar import Grammar
from ParsingTree import ParsingTree, Node

class Pair:
    def __init__(self, key, val):
        self.__key = key
        self.__val = val

    def __str__(self):
        return " {" + str(self.__key) + ", " + str(self.__val) + "}"

    def get_key(self):
        return self.__key

    def get_val(self):
        return self.__val

class Parser:
    def __init__(self, grammar):
        self.__grammar = grammar
        self.__firstList = {}
        self.__follow = {}
        self.__M = {}
        self.__err = None
        #self.__parsingTree = ParsingTree(None)
        self.__parseTable = []

    def create_empty_first(self):
        for nont in self.__grammar.getNonTerms():
            self.__firstList[nont] = set()

    def createFirstSet(self):
        self.create_empty_first()
        for nonT in self.__grammar.getNonTerms():
            self.__firstList[nonT] = self.first(nonT)


    '''
    Preconditions: nonterminal : String
    Postconditions: returns the set of first terminals
                    of given nonterminal, or empty set otherwise
    '''
    def first(self, nonterminal):
        if nonterminal in self.__firstList.keys() and len(self.__firstList[nonterminal]) > 0:
            return self.__firstList[nonterminal]

        terminals = self.__grammar.getAlphabet()
        productions = self.__grammar.getProductionsForSymbol(nonterminal)
        firstTerminals = set()

        for rhs in productions:
            if rhs == "epsilon":
                firstTerminals.add(rhs)
            else:
                productions_list = rhs.split(" ")
                count = 0
                for i in range(len(productions_list)):
                    firstSymbol = productions_list[i]
                    if count >= 1:
                        break
                    if firstSymbol in terminals:
                        firstTerminals.add(firstSymbol)
                        count += 1
                    else:
                        if firstSymbol != nonterminal and ("epsilon" in firstTerminals or len(firstTerminals) == 0):
                            aux=self.first(firstSymbol)
                            self.__firstList[firstSymbol] |= aux
                            firstTerminals |= aux
                            if "epsilon" not in aux:
                                break
                        else:
                            if firstSymbol != nonterminal:
                                aux = self.first(firstSymbol)
                                firstTerminals |= aux
                            break

        return firstTerminals

    def getFirst(self):
        self.createFirstSet()
        return self.__firstList

    def getFollow(self):
        self.create_follow()
        self.follow()
        return self.__follow

    def create_follow(self):
        for nont in self.__grammar.getNonTerms():
            self.__follow[nont] = set()


    '''
    Preconditions: nonTerm : String
    Postconditions: returns a list containing elements of type [A, y], 
                    where those respect the condition A -> a B y, or 
                    empty list otherwise
    '''
    def giveProductionsForFollow(self, nonTerm):
        result = []
        productions = self.__grammar.getProductions()

        for key in productions.keys():
            for i in range (len(productions[key])):
                if productions[key][i] != "epsilon":
                    elems = productions[key][i].split(" ")
                    if len(elems) >= 2 and nonTerm in elems:
                        i = 0
                        while elems[i] != nonTerm:
                            i += 1

                        result.append([key, elems[i+1:]])

        return result


    '''
    Preconditions: None
    Postconditions: return the set self.__follow, containg the 
                    terminals which follow the keys of the set (nonterminals)
                    Ex: self.__follow[A] contains terminals which follow nonterminal A, 
                    or epsilon if no terminal follows A.
    '''
    def follow(self):
        self.createFirstSet()

        self.__follow[self.__grammar.getStartingSymb()].add("epsilon")

        repeat = True

        while repeat:
            temp=self.__follow

            for nont in self.__grammar.getNonTerms():
                aux = self.giveProductionsForFollow(nont)
                for elem in aux:
                    a = elem[0]
                    y = elem[1]

                    if y == []:
                        self.__follow[nont] |= self.__follow[a]

                    for y1 in y:
                        if y1 in self.__grammar.getAlphabet():
                            self.__follow[nont].add(y1)
                            break
                        if y1 in self.__firstList.keys():
                            if "epsilon" in self.__firstList[y1]:
                                self.__follow[nont] |= self.__follow[a]
                                aux = self.__firstList[y1]
                                aux.remove("epsilon")
                                self.__follow[nont] |= aux
                            else:
                                self.__follow[nont] |= self.__firstList[y1]
                                break

            if temp==self.__follow:
                repeat=False

        return self.__follow

    def get_first_of_sequence(self, seq):
        p = seq.split(" ")
        first_seq = set()
        eps_count = 0
        for i in range(len(p)):
            if p[i] in self.__grammar.getAlphabet():
                first_seq.add(p[i])
                break
            elif p[i] in self.__grammar.getNonTerms():
                if "epsilon" in self.__firstList[p[i]]:
                    first_seq |= self.__firstList[p[i]]
                    first_seq.remove("epsilon")
                    eps_count += 1
                else:
                    first_seq |= self.__firstList[p[i]]
                    break

        if eps_count == len(p):
            first_seq.add("epsilon")

        return first_seq

    def construct_M_table(self):
        self.create_follow()
        self.follow()

        for terminal in self.__grammar.getAlphabet():
            self.__M[(terminal, terminal)] = ["pop"]

        self.__M[("$", "$")] = ["acc"]

        for nonTerminal in self.__grammar.getNonTerms():
            prod = self.__grammar.getProductionsForSymbol(nonTerminal)
            for terminal in self.__grammar.getAlphabet():
                for rhs in prod:
                    p = rhs.split(" ")
                    if (nonTerminal, terminal) not in self.__M.keys():
                        if terminal in p and terminal != "epsilon":
                            self.__M[(nonTerminal, terminal)] = [rhs, self.__grammar.get_production_number(nonTerminal, rhs)]
                        else:
                            if "epsilon" in self.get_first_of_sequence(rhs) and terminal in self.__follow[nonTerminal]:
                                self.__M[(nonTerminal, terminal)] = [rhs, self.__grammar.get_production_number(nonTerminal, rhs)]
                            elif "epsilon" not in self.get_first_of_sequence(rhs) and terminal in self.get_first_of_sequence(rhs):
                                self.__M[(nonTerminal, terminal)] = [rhs, self.__grammar.get_production_number(nonTerminal, rhs)]

        for nonTerminal in self.__grammar.getNonTerms():
            prod = self.__grammar.getProductionsForSymbol(nonTerminal)
            if "epsilon" in prod:
                i = self.__grammar.get_production_number(nonTerminal, "epsilon")
                self.__M[(nonTerminal, "$")] = ["epsilon", i]
                for terminal in self.__grammar.getAlphabet():
                    if terminal in self.__follow[nonTerminal] and (nonTerminal, terminal) not in self.__M.keys():
                        self.__M[(nonTerminal, terminal)] = ["epsilon", i]


    def get_table(self):
        self.construct_M_table()
        return self.__M

    def parse(self, w):
        aux = w.split(" ")
        alpha = []
        alpha += aux
        alpha.append("$")
        alpha.reverse()
        beta = [ self.__grammar.getStartingSymb(), "$"]
        beta.reverse()
        pi = []
        go = True
        s = ""
        self.construct_M_table()

        while go:
            if (beta[len(beta) - 1], alpha[len(alpha) - 1]) in self.__M.keys():
                aux = self.__M[(beta[len(beta) - 1], alpha[len(alpha) - 1])]
                if len(aux) == 1:
                    if aux[0] == "pop":
                        del beta[len(beta) - 1]
                        #beta.remove(beta[len(beta) - 1])
                        del alpha[len(alpha) - 1]
                    elif aux[0] == "acc":
                        go = False
                        s = "acc"
                    else:
                        go = False
                        s = "err"
                else:
                    [b, i] = aux
                    auxB=b.split(" ")
                    auxB.reverse()
                    if(len(auxB)>1):
                        del beta[len(beta)-1]
                        beta += auxB
                    else:
                        if(auxB[0]!="epsilon"):
                            beta[len(beta) - 1] = auxB[0]
                        else:
                            del beta[len(beta) - 1]

                    pi.append(i)
            else:
                go = False
                s = "err"
                self.__err = (beta[len(beta) - 1], alpha[len(alpha) - 1])
                print(self.__err)

        return (s, pi)

    def construct_parsing_table(self, sequence):
        res, self.__pi = self.parse(sequence)
        cnt = 1
        if res == "acc":
            for i in range (len(self.__pi)):
                prod = self.__grammar.get_production_by_number(self.__pi[i])

                if len(self.__parseTable) == 0:
                    self.__parseTable.append(Pair(cnt, Pair(prod[1], Pair(-1, -1))))
                    cnt += 1

                    p = prod[0].split(" ")
                    self.__parseTable.append(Pair(cnt, Pair(p[0], Pair(self.get_tabel_index(prod[1], 0), -1))))
                    cnt += 1
                    for j in range (1, len(p)):
                        if prod[1] in p[:j-1]:
                            self.__parseTable.append(Pair(cnt, Pair(p[j], Pair(self.get_tabel_index(prod[1], 1), cnt - 1))))
                        else:
                            self.__parseTable.append(
                                Pair(cnt, Pair(p[j], Pair(self.get_tabel_index(prod[1], 0), cnt - 1))))
                        cnt += 1
                else:
                    p = prod[0].split(" ")
                    self.__parseTable.append(Pair(cnt, Pair(p[0], Pair(self.get_tabel_index(prod[1], 0), -1))))
                    cnt += 1
                    for j in range(1, len(p)):
                        if prod[1] in p[:j-1]:
                            self.__parseTable.append(
                                Pair(cnt, Pair(p[j], Pair(self.get_tabel_index(prod[1], 1), cnt - 1))))
                        else:
                            self.__parseTable.append(
                                Pair(cnt, Pair(p[j], Pair(self.get_tabel_index(prod[1], 0), cnt - 1))))
                        cnt += 1


    def get_tabel_index(self, father, is_siblig):
        i = len(self.__parseTable) - 1
        cnt = 0
        if is_siblig:
            cnt = 1
        while i >= 0:
            if self.__parseTable[i].get_val().get_key() == father:
                if cnt == 0:
                    return self.__parseTable[i].get_key()
                else:
                    cnt -= 1
            i -= 1




    def create_parse_table(self):
        self.construct_parsing_table("a + ( a * a )")

        for p in self.__parseTable:
            print(str(p))

    def create_table(self, pi):
        for i in range (len(pi)):
            prod = self.__grammar.get_production_by_number(pi[i])

            if self.__parsingTree.get_root() == None:
                self.__parsingTree.set_root(Node(prod[1]))
                p = prod[0].split(" ")

                for p1 in p:
                    self.__parsingTree.add_child(Node(p1))
            else:
                p = prod[0].split(" ")
                self.__parsingTree.search_and_insert(0, prod[1], p)


    def tree_inorder(self):
        self.__parsingTree.inorder(self.__parsingTree.get_root())