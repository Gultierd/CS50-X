#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long number = get_long("Enter a number: "); // getting input from user
    int sum = 0;
    int length = 0;
    int lastNumbers = 0; // sum by Luhn's Algorithm, long length, first two digits of number
    while (number > 0)
    {
        length++;
        if (number > 10)
            lastNumbers = number % 100; // getting last two numbers
        sum += number % 10;             // increasing sum by luhn's
        number = number / 10;           // decreasing the number
        if (number > 0)
        {
            length++;
            if (number > 10)
                lastNumbers = number % 100;
            int tempProduct = number % 10 * 2; // tempproduct might be >10
            while (tempProduct > 0)
            {
                sum += tempProduct % 10; // adding each of tempproduct digtits to sum
                tempProduct = tempProduct / 10;
            }
            number = number / 10; // decreasing the number
        }
    }
    if (sum % 10 == 0) // veryfying by Luhn's algorithm
    {
        if (length == 13) // veryfing by length and last numbers
        {
            if (lastNumbers / 10 == 4)
                printf("VISA\n");
            else
                printf("INVALID\n");
        }
        else if (length == 15)
        {
            if (lastNumbers == 34 || lastNumbers == 37)
                printf("AMEX\n");
            else
                printf("INVALID\n");
        }
        else if (length == 16)
        {
            if (lastNumbers == 51 || lastNumbers == 52 || lastNumbers == 53 || lastNumbers == 54 ||
                lastNumbers == 55)
                printf("MASTERCARD\n");
            else if (lastNumbers / 10 == 4)
                printf("VISA\n");
            else
                printf("INVALID\n");
        }
        else
            printf("INVALID\n");
    }
    else
        printf("INVALID\n");
}
