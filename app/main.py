import sys


def main():
    
    while True:
        sys.stdout.write("$ ")
        command = input()
        print("{}: command not found".format(command))
        pass


if __name__ == "__main__":
    main()
