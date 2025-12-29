#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int compute(string word, int points[]);

int main(void)
{
    string p1 = get_string("Player 1: "); // getting input for player 1
    int p1length = strlen(p1);
    printf("size: %i\n", p1length);

    string p2 = get_string("Player 2: "); // getting input for player 2
    int p2length = strlen(p2);
    printf("size: %i\n", p2length);

    int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    // int array to hold points for each letter - can modify

    int score = compute(p1, points) - compute(p2, points); // calculating total score of each player

    if (score > 0)
    {
        printf("Player 1 wins!\n");
    }
    else if (score < 0)
    {
        printf("Player 2 wins!\n");
    }
    else
        printf("Tie!\n");
}

int compute(string word, int points[])
{
    int score = 0;
    for (int i = 0; i < strlen(word); i++) // going over each character in given word
    {
        char current = tolower(word[i]);
        score += points[current - 'a']; // increasing score according to points array
    }
    return score;
}
