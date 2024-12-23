#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Change owed: ");
    }
    while (n < 1);

    int m = 0;
    do
    {
        if (n >= 25)
        {
            n = n - 25;
            m = m + 1;
        }
        else if (n >= 10)
        {
            n = n - 10;
            m = m + 1;
        }
        else if (n >= 5)
        {
            n = n - 5;
            m = m + 1;
        }
        else if (n >= 1)
        {
            n = n - 1;
            m = m + 1;
        }
    }
    while (n != 0);

    printf("%i\n", m);
}
