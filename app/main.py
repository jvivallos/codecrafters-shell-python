import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    command = input()
    print("{}: command not found".format(command))
    pass


if __name__ == "__main__":
    main()
