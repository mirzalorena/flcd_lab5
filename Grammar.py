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
        line = file.readline().strip()
        while line != "":
            delimiters = "->"
            regexPattern = '|'.join(map(re.escape, delimiters))
            tokens = re.split(regexPattern, line)

            if tokens[0] not in self.__productions.keys():
                self.__productions[tokens[0]] = [tokens[2]]
            else:
                self.__productions[tokens[0]].append(tokens[2])

            line = file.readline().strip()

        file.close()

def menu():
    print("0. Exit")
    print("1. Set of NonTerminals")
    print("2. The alphabet")
    print("3. Starting Symbol")
    print("4. Productions")

if __name__ == '__main__':
    print("Test Grammar")
    menu()

    option=-1

    grammar = Grammar("file.in")

    while(option!=0):
        option=int(input("What do you wanna see?"))
        if option==1:
            print(grammar.getNonTerms())
        elif option==2:
            print(grammar.getAlphabet())
        elif option==3:
            print(grammar.getStartingSymb())
        elif option==4:
            print(grammar.getProductions())