// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 4100;

// Hash table
node *table[N];

int dictSize = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int value = hash(word);

    node *n = table[value];

    while (n != NULL)
    {
        if (strcasecmp(word, n->word) == 0)
        {
            return true;
        }

        n = n->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int value = 0;
    int length = strlen(word);

    for (int i = 0; i < length; i++)
    {
        value += toupper(word[i]);
    }

    return value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");

    if (dictionary == NULL)
    {
        printf("Dictionary not found");
        return false;
    }

    char word[LENGTH + 1];

    while (fscanf(dict, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, word);

        int value = hash(word);

        n->next = table[value];
        table[value] = n;

        dictSize += 1;
    }

    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dictSize;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];

        while (n != NULL)
        {
            node *temporary = n;
            n = n->next;

            free(temporary);
        }

        if (n == NULL && i == (N - 1))
        {
            return true;
        }
    }

    return false;
}
