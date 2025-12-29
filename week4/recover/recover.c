#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool checkFile(FILE *input, unsigned char byte, FILE *output);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover input.raw\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "rb");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    unsigned char buffer[512]; // we'll read files 512 bytes at once (FAT files)
    char jpg[8] = {'0', '0', '0', '.', 'j', 'p', 'g', '\0'};
    FILE *output = NULL;
    int number = 0;

    while (fread(&buffer, sizeof(buffer), 1, input) != 0) // while we still have some data
    {                                                     // checking for a new header
        if (buffer[0] == 255 && buffer[1] == 216 && buffer[2] == 255 && buffer[3] > 223 &&
            buffer[3] < 240)
        {
            // new output file, setting numbers
            jpg[0] = number / 100 + '0';
            jpg[1] = (number / 10) % 10 + '0';
            jpg[2] = number % 10 + '0';
            // closing last output
            if (output != NULL)
            {
                fclose(output);
            }
            // opening or creating a new one
            output = fopen(jpg, "w");
            number++;
        }
        if (output != NULL)
        {
            fwrite(&buffer, sizeof(buffer), 1, output);
        }
    }
    printf("%i\n", number);
    fclose(input);
    fclose(output);
}
