import csv
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py csv txt")
        sys.exit(1)

    with open(sys.argv[1], "r") as file:
        reader = csv.reader(file)
        database = list(reader)

    with open(sys.argv[2], "r") as file:
        sequences = file.read()

    match = []
    for i in range(1, len(database[0])):
        match.append(longest_match(sequences, database[0][i]))

    person = ""
    counter = 0
    for i in range(1, len(database)):
        for j in range(len(match)):
            if match[j] == int(database[i][j+1]):
                counter += 1
        if counter == len(match):
            person = database[i][0]
            break
        else:
            counter = 0
    else:
        print("No match")

    print(person)

    return


def longest_match(sequence, subsequence):

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
