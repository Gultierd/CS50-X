def main():
    print("Text: ", end="")
    text = input()  # getting user input
    grade = round(calculateIndex(text))  # calculating grade

    if (grade < 1):  # printing the result
        print("Before Grade 1")
    else:
        print("Grade ", end="")
        if (grade <= 16):
            print(grade)
        else:
            print("16+")


def calculateIndex(text):
    letters = 0
    sentences = 0
    words = 1
    text = text.lower()
    for i in range(len(text)):  # counting each character in given text
        current = text[i]
        if (current >= "a" and current <= "z"):
            letters += 1
        elif (current == " "):
            words += 1
        elif (current == "." or current == "?" or current == "!"):
            sentences += 1
    return ((0.0588 * letters * 100 / words) - (0.296 * sentences * 100 / words) - 15.8)


main()
