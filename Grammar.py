import re

class Grammar:
    def __init__(self, filename):
        self.__filename = filename
        self.__nonterminals = []
        self.__startingSymbol = None
        self.__alphabet = []
        self.__productions = {}
        self.readFromFile()

    def getNonTerms(self):
        return self.__nonterminals

    def getStartingSymb(self):
        return self.__startingSymbol

    def getAlphabet(self):
        return self.__alphabet

    def getProductions(self):
        return self.__productions

    def getProductionsForSymbol(self, nonTerminal):
        if nonTerminal not in self.__productions.keys():
            return []
        return self.__productions[nonTerminal]

    def get_production_number(self, nonTerminal, rhs):
        i = 0
        stop = False

        for key in self.__productions.keys():
            if stop == True:
                break
            for p in self.__productions[key]:
                if key == nonTerminal:
                    if stop == True:
                        break
                    i += 1
                    if p == rhs:
                        stop = True
                        break
                else:
                    i += 1

        return i

    def get_production_by_number(self, number):
        prod = None
        i = 1
        stop = False
        for key in self.__productions.keys():
            if stop == True:
                break 
            for p in self.__productions[key]:
                if stop == True:
                    break 
                if i == number:
                    stop = True 
                    prod = p 
                    break
                i += 1
                
        return prod
                

    def readFromFile(self):
        file = open(self.__filename, 'r')
        line = file.readline().strip()

        # read the nonterminals
        delimiters = "--", "{", "}"
        regexPattern = '|'.join(map(re.escape, delimiters))
        tokens = re.split(regexPattern, line)

        nonterminals = tokens[2].split(",")

        for nont in nonterminals:
            self.__nonterminals.append(nont)

        #read the alphabet
        line = file.readline().strip()
        delimiters = "--", "{", "}"
        regexPattern = '|'.join(map(re.escape, delimiters))
        tokens = re.split(regexPattern, line)
        alphabet = tokens[2].split(",")

        for alpha in alphabet:
            self.__alphabet.append(alpha)

        self.__alphabet.append("{")
        self.__alphabet.append("}")

        #read the starting symbol
        line = file.readline().strip()
        token = line.split("--")
        self.__startingSymbol = token[1]

        #read the productions
        line = file.readline().strip()
        while line != "":
            delimiters = "->"
            regexPattern = '|'.join(map(re.escape, delimiters))
            tokens = re.split(regexPattern, line)
            if tokens[2] == '':
                tokens[2] = '-'

            if tokens[0] not in self.__productions.keys():
                self.__productions[tokens[0]] = [tokens[2]]
            else:
                self.__productions[tokens[0]].append(tokens[2])

            line = file.readline().strip()

        if "relation" in self.__productions.keys():
            self.__productions["relation"].append(">")

        file.close()

