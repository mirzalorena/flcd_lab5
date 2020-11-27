from Grammar import Grammar

class Parser:
    def __init__(self, grammar):
        self.__grammar = grammar
        self.__firstList = {}
        self.__follow = {}

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