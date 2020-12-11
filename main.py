from Parser import Parser
from Grammar import Grammar
import sys

def menu():
    print("0. Exit")
    print("1. Set of NonTerminals")
    print("2. The alphabet")
    print("3. Starting Symbol")
    print("4. Productions")
    print("5. Get productions for a given non-terminal")
    print("6. Get first list ")
    print("7. Get follow")
    print("8. LL1 Parsing Table for sequence")
    print("9. Create parsing table for sequence")

if __name__ == '__main__':
    print("Test Grammar")
    menu()

    option=-1

    sys.setrecursionlimit(5000000)

    grammar = Grammar("file.in")
    parser = Parser(grammar)

    #parser.create_parse_table()

    #print(parser.parse("individual a ; a = 2 ;"))

    #print(parser.parse("individual a ; individual b ; individual g ; come a ; come b ; parsing ( a != b ) { situation ( a > b ) { a = a - b ; } other { b = b - a ; } } g = a - 0 ; leave g ;"))

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
        elif option == 5:
            nont = input("Please give a non-terminal: ")
            print(grammar.getProductionsForSymbol(nont))
        elif option == 6:
            print(parser.getFirst())
        elif option==7:
            print(parser.getFollow())
        elif option==8:
            seq=input("Give a sequence: ")
            print(parser.parse(seq))
        elif option==9:
            parser.create_parse_table()
