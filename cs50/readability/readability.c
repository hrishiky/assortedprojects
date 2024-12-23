#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int getWords(string paragraph);
int getLetters(string paragraph);
int getSentences(string paragraph);

int main(void)
{
    string text = get_string("Text: ");

    int words = getWords(text);
    int letters = getLetters(text);
    int sentences = getSentences(text);
    // printf("Words: %i\nLetters: %i\nSentences: %i\n", words, letters, sentences);

    float L = ((float) letters / (float) words) * 100.0;
    // printf("L: %f\n", L);
    float S = ((float) sentences / (float) words) * 100.0;
    // printf("S: %f\n", S);
    float floatIndex = 0.0588 * L - 0.296 * S - 15.8;
    // printf("floatindex: %f\n", floatIndex);
    int index = round(floatIndex);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int getWords(string paragraph)
{
    int words = 0;
    int length = strlen(paragraph);

    for (int i = 0; i < length; i++)
    {
        if (paragraph[i] == ' ' || (paragraph[i] == '.' && paragraph[i + 1] != ' ') ||
            (paragraph[i] == '?' && paragraph[i + 1] != ' ') ||
            (paragraph[i] == '!' && paragraph[i + 1] != ' '))
        {
            words += 1;
        }
    }

    return words;
}

int getLetters(string paragraph)
{
    int letters = 0;
    int length = strlen(paragraph);

    for (int i = 0; i < length; i++)
    {
        if (isalpha(paragraph[i]))
        {
            letters += 1;
        }
    }

    return letters;
}

int getSentences(string paragraph)
{
    int sent = 0;
    int length = strlen(paragraph);

    for (int i = 0; i < length; i++)
    {
        if (paragraph[i] == '.' || paragraph[i] == '!' || paragraph[i] == '?')
        {
            sent += 1;
        }
    }

    return sent;
}
