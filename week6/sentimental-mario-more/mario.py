def main():  # declaring main method
    h = 'a'
    while (not (type(h) == int) or h < 1 or h > 8):  # getting user input
        print("Height from 1 to 8: ", end="")
        h = input()
        if (h.isnumeric()):
            h = int(h)
    pyramid(h)  # creating a pyramid


def pyramid(h):
    for i in range(h):  # printing each row
        row(i+1, h-i-1)
        print(end="\n")


def row(hash, space):
    for i in range(space):  # spaces before hashes
        print(" ", end="")
    for i in range(hash):
        print("#", end="")
    print("  ", end="")  # bridge
    for i in range(hash):
        print("#", end="")


main()
