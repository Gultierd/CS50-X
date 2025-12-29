#include <cs50.h>
#include <stdio.h>

void pyramids(int height);
void bridge(int length);
void row(int hash, int space); // methods prototypes

int main(void)
{
    int height;
    do
    {
        height = get_int(
            "How tall the pyramids should be? Select from 1 to 8: "); // requesting data from user
    }
    while (1 > height || height > 8); // data between 1 to 8 inclusive
    pyramids(height); // using method to draw pyramids
}

void pyramids(int height)
{
    for (int i = 1; i <= height; i++) // drawing each row
    {
        row(i, (height - i));
        printf("\n"); // new line between rows
    }
}

void row(int hash, int space)
{
    for (int i = 0; i < space; i++)
    {
        printf(" ");
    }
    for (int i = 0; i < hash; i++)
    {
        printf("#");
    }
    bridge(2);
    for (int i = 0; i < hash; i++)
    {
        printf("#");
    }
}

void bridge(int length)
{
    for (int i = 0; i < length; i++)
    {
        printf(" ");
    }
}
