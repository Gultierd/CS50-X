// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    uint8_t header[HEADER_SIZE]; // allocating memory for header

    if (fread(&header, HEADER_SIZE, 1, input) != 0) // if we can read the header correctly
    {
        fwrite(&header, HEADER_SIZE, 1, output); // we write it to output file
    }

    int16_t bytes;

    while (fread(&bytes, sizeof(bytes), 1, input) != 0)
    {
        bytes *= factor;                          // we multiply by given factor
        fwrite(&bytes, sizeof(bytes), 1, output); // writing to file
    }

    // Close files
    fclose(input);
    fclose(output);
}
