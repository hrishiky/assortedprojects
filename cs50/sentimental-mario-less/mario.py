from cs50 import get_int


while True:
    try:
        n = get_int("Height: ")
        if (n >= 1) and (n <= 8):
            break
    except:
        pass

m = n - 1
o = 1

for i in range(n):
    for j in range(m):
        print(" ", end="")
    m -= 1

    for k in range(o):
        print("#", end="")
    o += 1

    print()
