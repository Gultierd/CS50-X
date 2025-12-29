#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2) // verifying arguments
    {
        printf("Invalid arguments - only 1 argument containing 26 letters\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26) // veryfying key length
    {
        printf("Invalid key size - must contain 26 different letters\n");
        return 1;
    }
    int lookUpTable[26] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // array for all letters
    for (int i = 0; i < 26; i++)                                   // veryfying key values
    {
        char c = argv[1][i];
        if (!(('a' <= c && c <= 'z') ||
              ('A' <= c && c <= 'Z'))) // only letters - lowercase and uppercase allowed
        {
            printf("Invalid characters in key - must contain only letters\n");
            return 1;
        }
        else if ('a' <= c && c <= 'z')
        {
            lookUpTable[c - 'a']++; // increasing corresponding value in lookUpTable to verify
                                    // amount of usages
            if (lookUpTable[c - 'a'] > 1)
            {
                printf("Invalid characters in key - cannot contain duplicates!\n");
                return 1;
            }
        }
        else if ('A' <= c && c <= 'Z')
        {
            lookUpTable[c - 'A']++; // increasing corresponding value in lookUpTable to verify
                                    // amount of usages
            if (lookUpTable[c - 'A'] > 1)
            {
                printf("Invalid characters in key - cannot contain duplicates!\n");
                return 1;
            }
        }
    }
    // arguments veryfied - now get user input
    string userInput = get_string("plaintext: ");
    for (int i = 0; i < strlen(userInput); i++)
    {
        char c = userInput[i];
        if ('a' <= c && c <= 'z') // swapping lowercase letters
        {
            userInput[i] = tolower(argv[1][c - 'a']);
        }
        else if ('A' <= c && c <= 'Z') // swapping uppercase letters
        {
            userInput[i] = toupper(argv[1][c - 'A']);
        }
    }
    printf("ciphertext: %s\n", userInput);
}
