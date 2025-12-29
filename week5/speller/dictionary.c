// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
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
const unsigned int N = 6151;

// Hash table
node *table[N];
int dictionarySize = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    node *currentNode = table[hash(word)];

    while (currentNode != NULL)
    {
        if (strcasecmp(word, currentNode->word) == 0)
        {
            return true;
        }

        currentNode = currentNode->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int n = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        n = n + tolower(word[i]);
    }
    return n % 6151;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *input = fopen(dictionary, "r");
    char word[45];

    while (fscanf(input, "%s", word) != EOF) // while new words exist
    {
        node *currentNode = malloc(sizeof(node));

        if (currentNode == NULL)
        {
            return false;
        }

        strcpy(currentNode->word, word);

        // TODO: hashing and inserting to hashtable
        int h = hash(word);
        currentNode->next = table[h];
        table[h] = currentNode;
        dictionarySize++;
    }

    fclose(input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dictionarySize;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    { // for each bucket in our hashTable
        node *currentNode = table[i];

        while (currentNode != NULL)
        {
            node *temp = currentNode->next; // saving pointer to next node
            free(currentNode);              // freeing last node
            currentNode = temp;             // going over to next node
        }
    }
    dictionarySize = 0;
    return true;
}
