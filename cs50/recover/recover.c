#include <stdio.h>
#include <stdlib.h>

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover file\n");
        return 1;
    }

    char *input = argv[1];
    FILE *inputPointer = fopen(input, "r");

    if (input == NULL)
    {
        printf("Input file not found\n");
        return 2;
    }

    unsigned char buffer[BLOCK_SIZE];
    int imageCounter = 0;
    FILE *outputPointer = NULL;
    int jpegFound = 0;

    while (fread(&buffer, BLOCK_SIZE, 1, inputPointer) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpegFound == 1)
            {
                fclose(outputPointer);
            }
            else
            {
                jpegFound = 1;
            }

            char filename[8];
            sprintf(filename, "%03i.jpg", imageCounter);

            outputPointer = fopen(filename, "w");

            imageCounter += 1;
        }

        if (jpegFound == 1)
        {
            fwrite(&buffer, BLOCK_SIZE, 1, outputPointer);
        }
    }

    fclose(inputPointer);
    fclose(outputPointer);

    return 0;
}
