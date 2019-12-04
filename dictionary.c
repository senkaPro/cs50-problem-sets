// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

// Represents a trie
node *root;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = malloc(sizeof(node));
    if (root == NULL)
    {
        return false;
    }
    root->is_word = false;
    for (int i = 0; i < N; i++)
    {
        root->children[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        node *children = root;

        for(int i = 0; word[i] != '\0'; i++)
        {
            int index = (word[i] == '\'') ? N - 1 : word[i] - 'a';

            if(children->children[index] == NULL)
            {
                node * nextChild = malloc(sizeof(node));
                if(nextChild == NULL)
                {
                    unload();
                    return false;
                }
                nextChild->is_word = false;

                for(int j = 0; j < N; j++)
                {
                    nextChild->children[j] = NULL;
                }

                children->children[index] = nextChild;

                if(i == 0)
                {
                    root->children[index] = nextChild;
                }
            }

            children = children->children[index];
        }

        children->is_word = true;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if(!root)
    {
        return 0;
    }

    int word_count = 0;

    node *ptr = root;

    if(ptr->is_word)
    {
        word_count++;
    }

    for(int i = 0; i < N; i++)
    {
        root = ptr->children[i];

        word_count += size();
    }

    root = ptr;

    return word_count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    if(!root)
    {
        return false;
    }

    node *ptr = root;

    for(int i = 0; word[i] != '\0'; i++)
    {
        char c = tolower(word[i]);
        int index = (c == '\'') ? N - 1 : c - 'a';

        if(!ptr->children[index])
        {
            return false;
        }

        ptr = ptr->children[index];
    }

    return ptr->is_word;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    if(!root)
    {
        return false;
    }
    node *ptr = root;

    for(int i = 0; i < N; i++)
    {
        root = ptr->children[i];
        unload();
    }

    root = ptr;

    free(ptr);

    return true;
}
