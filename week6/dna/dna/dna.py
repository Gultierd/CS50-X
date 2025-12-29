import csv
import sys


def main():

    # Check for command-line usage
    if (len(sys.argv) != 3):
        print("Incorrect arguments - usage: dna.py database.csv sequence.txt")
        return

    # Read database file into a variable
    file = csv.DictReader(open(sys.argv[1]))
    names = []       # making arrays for names
    values = []      # and for corresponding dataset
    for row in file:  # saving data to each array
        seq = []
        for i in file.fieldnames[1:]:
            seq.append(int(row[i]))
        names.append(row["name"])
        values.append(seq)
    # Read DNA sequence file into a variable
    sequence = open(sys.argv[2], "r").read()

    # Find longest match of each STR in DNA sequence
    list = []  # array holding longest matches for sets
    for i in file.fieldnames[1:]:
        list.append(longest_match(sequence, i))

    # Check database for matching profiles
    match = "No match"  # at the beggining we have no match
    for i in range(len(names)):
        if (values[i] == list):
            match = names[i]

    print(match)
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

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
