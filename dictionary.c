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

//Tracking dictionary loaded state
bool loaded = false;

//Tracking word count
unsigned int word_counter = 0;

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
        //set children's value
        node * children = root;

        //Loop throught char in word
        for (int i = 0; word[i] != '\0'; i++)
        {
            //Get char index
            int index = (word[i] == '\'') ? N-1 : word[i] - 'a';

            //Is the pointer to the char NULL
            if(children->children[index] == NULL)
            {
                //Create node to be pointed by the char index
                node * nextChild = malloc(sizeof(node));
                if(nextChild == NULL)
                {
                    unload();
                    return false;
                }
                nextChild->is_word = false;

                for (int j = 0; j < N; j++)
                {
                    nextChild->children[j] = NULL;
                }

                //Point the index to the new node
                children->children[index] = nextChild;

                //If its first char in the word point the root to new node
                if(i == 0)
                {
                    root->children[index] = nextChild;
                }
            }

            //Pointing to the next node
            children = children->children[index];
        }

        //End of the word true
        children->is_word = true;
        word_counter++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    loaded = true;
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (loaded)
    {
        return word_counter;
    }
    else
    {
        return 0;
    }
    return 0;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //Check if dictionary loaded
    if(!loaded)
    {
        return false;
    }

    node *ptr = root;

    for(int i = 0; word[i] != '\0'; i++)
    {
        char ch = tolower(word[i]);
        int index = (ch == '\'') ? N - 1 : ch - 'a';

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
    // TODO
    if(!loaded)
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
