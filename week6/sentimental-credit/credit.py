def main():
    print("Enter a card number: ", end="")
    number = input()  # getting user input
    while (not (number.isnumeric())):  # if not a number - request again
        print("Enter a card number: ", end="")
        number = input()
    firstNumbers = number[0] + number[1]  # leading digits
    if (luhn(number)):  # verifying by luhn's algorithm
        if (firstNumbers in ["34", "37"] and len(number) == 15):
            print("AMEX")
        elif (firstNumbers in ["51", "52", "53", "54", "55"] and len(number) == 16):
            print("MASTERCARD")
        elif (firstNumbers[0] == "4" and ((len(number) == 13) or (len(number) == 16))):
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")


def luhn(number):
    number = int(number)
    length = 0
    sum = 0
    while (number > 0):
        length += 1
        sum += number % 10
        number = int(number / 10)
        if (number > 0):
            length += 1
            tempProduct = (number % 10) * 2
            while (tempProduct > 0):
                sum += tempProduct % 10
                tempProduct = int(tempProduct / 10)
            number = int(number / 10)
    if (sum % 10 == 0):
        return True
    return False


main()
