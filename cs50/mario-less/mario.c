#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    int m = n - 1;
    int o = 1;

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            printf(" ");
        }
        m = m - 1;

        for (int k = 0; k < o; k++)
        {
            printf("#");
        }
        o = o + 1;

        printf("\n");
    }
}
