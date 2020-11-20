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

        first_terminals = []
        terminals = self.__grammar.getAlphabet()
        productions = self.__grammar.getProductionsForSymbol(nonterminal)

        for rhs in productions:
            firstSymbol = rhs[0]

            if firstSymbol == "epsilon" or firstSymbol in terminals:
                first_terminals.append(firstSymbol)
            else:
                if len(first_terminals) == 0:
                    first_terminals += self.first(firstSymbol)

        return first_terminals


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
            elems=list(productions[key])
            if(nonTerm in elems):
                position=elems.index(nonTerm)
                if position>1 and position<len(elems)-1:
                    result.append([key,productions[:position]])

        return result

    def follow(self):
        self.createFirstSet()

        self.__follow[self.__grammar.getStartingSymb()] = "epsilon"

        repeat = True

        while repeat:
            temp=self.__follow

            for nont in self.__grammar.getNonTerms():
                aux = self.checkFollowForm(nont)
                for elem in aux:
                    a = elem[0]
                    y = elem[1]
                    if y in self.__firstList.keys():
                        if "epsilon" in self.__firstList[y]:
                            self.__follow[nont]=self.__follow[nont]+self.__follow[a]
                        else :
                            self.__follow[nont]=self.__follow[nont]+self.__firstList[y]

            if temp==self.__follow:
                repeat=False

        return self.__follow





