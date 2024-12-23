from cs50 import get_string


def main():
    text = get_string("Text: ")

    i = 0
    words = 0
    letters = 0
    sentences = 0
    length = len(text)

    while i < length:
        if (text[i].isalpha()):
            letters += 1
        if (i != length and text[i] == " " and text[i + 1] != " ") or (i == 0 and text[i] != " "):
            words += 1
        if (text[i] == "." or text[i] == "?" or text[i] == "!"):
            sentences += 1

        i += 1

    L = (letters / words) * 100.0
    S = (sentences / words) * 100.0
    index = round(0.0588 * L - 0.296 * S - 15.8)

    if (index < 1):
        print("Before Grade 1")
    elif (index > 16):
        print("Grade 16+")
    else:
        print(f"Grade {index}")


main()
