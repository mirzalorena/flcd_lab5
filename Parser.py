from Grammar import Grammar

class Parser:
    def __init__(self, grammar):
        self.__grammar = grammar
        self.__firstList = {}
        self.__follow = {}

    def createFirstSet(self):
        for nonT in self.__grammar.getNonTerms():
            self.__firstList[nonT] = self.first(nonT)

    def first(self, nonterminal):
        if nonterminal in self.__firstList.keys():
            return self.__firstList[nonterminal]

        terminals = self.__grammar.getAlphabet()
        productions = self.__grammar.getProductionsForSymbol(nonterminal)
        firstTerminals = set()

        for rhs in productions:
            if rhs == "epsilon":
                firstTerminals.add(rhs)
            else:
                productions_list = list(rhs)
                count = 0
                for i in range(len(productions_list)):
                    firstSymbol = rhs[i]
                    if count >= 1:
                        break
                    if firstSymbol in terminals:
                        firstTerminals.add(firstSymbol)
                        count += 1
                    else:
                        if firstSymbol != nonterminal:
                            firstTerminals |= self.first(firstSymbol)

        return firstTerminals


    def getFirst(self):
        self.createFirstSet()
        return self.__firstList

    def getFollow(self):
        self.follow()
        return self.__follow

    def checkFollowForm(self,nonTerm):
        result=[]

        productions=self.__grammar.getProductions()

        for key in productions.keys():
            if productions[key][0] != "epsilon":
                elems=list(productions[key][0])
                if(nonTerm in elems):
                    position=elems.index(nonTerm)
                    if position>=1 and position<len(elems)-1:
                        result.append([key,elems[position:]])

        return result

    def follow(self):
        self.createFirstSet()

        self.__follow[self.__grammar.getStartingSymb()] = {"epsilon"}

        repeat = True

        while repeat:
            temp=self.__follow

            for nont in self.__grammar.getNonTerms():
                aux = self.checkFollowForm(nont)
                for elem in aux:
                    a = elem[0]
                    y = elem[1]
                    for y1 in y:
                        if y1 in self.__firstList.keys():
                            if "epsilon" in self.__firstList[y1]:
                                if nont in self.__follow.keys():
                                    self.__follow[nont] |= self.__follow[a]
                                else:
                                    self.__follow[nont] = self.__follow[a]
                            else :
                                if nont not in self.__follow.keys():
                                    self.__follow[nont] = self.__firstList[y1]
                                else:
                                    self.__follow[nont] |= self.__firstList[y1]

            if temp==self.__follow:
                repeat=False

        return self.__follow





