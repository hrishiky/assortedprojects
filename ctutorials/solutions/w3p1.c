#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
  if (argc != 2 || strlen(argv[1]) != 1) {
    printf("Please input a single letter command line argument ('a' or 's')\n");
    return 1;
  }

  int x, y;
  printf("Please input a number: ");
  scanf("%d", &x);
  printf("Please input another number: ");
  scanf("%d", &y);

  if (argv[1][0] == 'a') {
    printf("%d + %d = %d\n", x, y, x+y);
  } else if (argv[1][0] == 's') {
    printf("%d - %d = %d\n", x, y, x-y);
  } else {
    printf("Please input a valid command line argument ('a' or 's')\n");
    return 1;
  }

  return 0;
}
