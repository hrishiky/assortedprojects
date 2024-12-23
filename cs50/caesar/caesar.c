#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool onlyNumbers(string key);
string caesarCipher(string plaintext, int key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    if (onlyNumbers(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int key = atoi(argv[1]);
    while (key > 26)
    {
        key -= 26;
    }

    string plaintext = get_string("plaintext: ");
    string ciphertext = caesarCipher(plaintext, key);
    printf("ciphertext: %s\n", ciphertext);
}

bool onlyNumbers(string key)
{
    bool onlyNum = true;

    for (int i = 0, length = strlen(key); i < length; i++)
    {
        if (isdigit(key[i]) == false)
        {
            onlyNum = false;
        }
    }

    return onlyNum;
}

string caesarCipher(string plaintext, int key)
{
    int length = strlen(plaintext);
    string ciphertext = plaintext;

    for (int i = 0; i < length; i++)
    {
        if (isalpha(plaintext[i]) == false)
        {
            ciphertext[i] = plaintext[i];
        }
        else
        {
            if (isupper(plaintext[i]))
            {
                if ((plaintext[i] + key) > 90)
                {
                    ciphertext[i] = (plaintext[i] - 26) + key;
                }
                else
                {
                    ciphertext[i] = plaintext[i] + key;
                }
            }
            else
            {
                if ((plaintext[i] + key) > 122)
                {
                    ciphertext[i] = (plaintext[i] - 26) + key;
                }
                else
                {
                    ciphertext[i] = plaintext[i] + key;
                }
            }
        }
    }

    return ciphertext;
}
