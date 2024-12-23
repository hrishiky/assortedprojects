from cs50 import get_float

while True:
    try:
        n = get_float("Change: ")
        if (n >= 0.01):
            break
    except:
        pass

m = 0
n = n * 100

while True:
    if (n >= 25):
        n -= 25
        m += 1
    elif (n >= 10):
        n -= 10
        m += 1
    elif (n >= 5):
        n -= 5
        m += 1
    elif (n >= 1):
        n -= 1
        m += 1
    if (n == 0):
        break

print(f"{m}")
