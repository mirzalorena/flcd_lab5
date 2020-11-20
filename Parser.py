from Grammar import Grammar

class Parser:
    def __init__(self, grammar):
        self.__grammar = grammar
        self.__firstList = {}

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




