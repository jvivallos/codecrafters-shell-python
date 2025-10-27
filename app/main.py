import sys


def main():
    
    while True:
        sys.stdout.write("$ ")
        command = input()

        if(command.startswith("exit 0")):
            return 0
        print("{}: command not found".format(command))
        


if __name__ == "__main__":
    main()
