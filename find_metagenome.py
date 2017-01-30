from load import load_nitrogenase_seq, load_metagenome
import time

debug = 0
python_vers = 2


def print_debug(*str):
    if(debug):
        print(str)


def longest_common_substring(str1, str2):
    """ Returns list of the longest common substrings.

    str1, str2: strings to compare
    returns: list of the longest common substrings

    >>> longest_common_substring("123456789", "123898789798678979834312341234")
    ['1234', '1234', '6789']
    """

    length_substring = []
    cur_longest = 0
    ret = []

    for i in range(len(str1)):
        length_substring.append([0]*len(str2))
        for j in range(len(str2)):
            if(str1[i].upper() == str2[j].upper()):
                if(i == 0 or j == 0):
                    length_substring[i][j] = 1
                else:
                    length_substring[i][j] = length_substring[i-1][j-1] + 1

                # If current string is the longest, update cur_longest and ret
                if(length_substring[i][j] > cur_longest):
                    cur_longest = length_substring[i][j]
                    ret = [str1[i - cur_longest + 1:i + 1]]
                    print_debug("Found new longest:", cur_longest, "At:", i, j)
                    print_debug(str1[i - cur_longest + 1:i + 1], i - cur_longest + 1, i + 1)
                elif(length_substring[i][j] == cur_longest):
                    ret.append(str1[i - cur_longest + 1:i + 1])
                    print_debug("Found another string at:", i, j)
                    print_debug(str1[i - cur_longest + 1:i + 1], i - cur_longest + 1, i + 1)

    if(debug):
        for i in range(len(str1)):
            print(length_substring[i])

    return ret


def find_all_substrings(genomes, sequence):
    """ Iterates through all genomes and searches for the longest substring of the sequence in each """

    if(python_vers == 3):
        time_curr = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
    else:
        time_curr = time.clock()
    print(time_curr)

    genomes_len = len(genomes)

    substrings = []

    for i in range(genomes_len):
        substrings.append(longest_common_substring(genomes[i][1], sequence))

        if(python_vers == 3):
            time_last = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID) - time_curr
            time_curr = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
            # print('[', time_last, 's] [total: ', time_curr, 's]', sep='') # Needs to be commented out for pypy

        else:
            time_last = time.clock() - time_curr
            time_curr = time.clock()
            print i, '/', genomes_len, '[', time_last, 's] [total: ', time_curr, 's]'

    return substrings


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    metagenome = load_metagenome()
    nitrogenase = load_nitrogenase_seq()

    print(find_all_substrings(metagenome[:50], nitrogenase))
