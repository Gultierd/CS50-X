#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

double calculateCLIndex(string input);

int main(void)
{
    string input = get_string("Text: "); // getting input from user
    int grade = round(calculateCLIndex(input));

    if (grade < 1)
        printf("Before Grade 1\n");
    else
    {
        printf("Grade ");
        if (grade <= 16)
            printf("%i\n", grade);
        else
            printf("16+\n");
    }
}

double calculateCLIndex(string input)
{
    int letters = 0;
    int sentences = 0;
    int words = 1; // necessary variables
    for (int i = 0; i < strlen(input); i++)
    {
        char current = tolower(input[i]);
        if (current <= 'z' && current >= 'a') // if character belongs to letters
            letters++;
        else if (current == ' ') // if character is a space (another word)
            words++;
        else if (current == '.' || current == '?' || current == '!') // if character ends a sentence
            sentences++;
    }
    return 0.0588 * (double) letters * 100 / (double) words -
           0.296 * (double) sentences * 100 / (double) words - 15.8;
}
