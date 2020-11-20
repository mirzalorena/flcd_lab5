import re

class Grammar:
    def __init__(self, filename):
        self.__filename = filename
        self.__nonterminals = []
        self.__startingSymbol = None
        self.__alphabet = []
        self.__productions = {}

    def readFromFile(self):
        file = open(self.__filename, 'r')
        line = file.readline().strip()

        # read the nonterminals
        delimiters = "=", "{", "}"
        regexPattern = '|'.join(map(re.escape, delimiters))
        tokens = re.split(regexPattern, line)

        nonterminals = tokens[2].split(",")

        for nont in nonterminals:
            self.__nonterminals.append(nont)

        #read the alphabet
        line = file.readline().strip()
        delimiters = "=", "{", "}"
        regexPattern = '|'.join(map(re.escape, delimiters))
        tokens = re.split(regexPattern, line)
        alphabet = tokens[2].split(",")

        for alpha in alphabet:
            self.__alphabet.append(alpha)

        #read the starting symbol
        line = file.readline().strip()
        token = line.split("=")
        self.__startingSymbol = token[1]

        #read the productions
        line = file.read().strip()
        while line != "":
            delimiters = "-", ">"
            regexPattern = '|'.join(map(re.escape, delimiters))
            tokens = re.split(regexPattern, line)

            if tokens[0] not in self.__productions.keys():
                self.__productions = [tokens[1]]
            else:
                self.__productions[tokens[0]].append(tokens[1])

            line = file.readline().strip()

        file.close()