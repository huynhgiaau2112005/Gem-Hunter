import sys
from menu import Menu
from argument_handler import ArgumentHandler

def main_business():
    if len(sys.argv) == 1:
        Menu().execute()
    elif len(sys.argv) == 3:
        ArgumentHandler().execute()
    else:
        print("Invalid Arguments")
    
def main():
    main_business()

if __name__ == "__main__":
    main()