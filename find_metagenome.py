from load import load_nitrogenase_seq, load_metagenome
import time
from multiprocessing import Pool

""" Multithread version. For python2.7, pypy

Base time: 57s"""


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

                elif(length_substring[i][j] == cur_longest):
                    ret.append(str1[i - cur_longest + 1:i + 1])

    return ret


def find_all_substrings(genomes):
    """ Iterates through all genomes and searches for the longest substring of the sequence in each """

    # print genomes[1]
    # print
    # print '*' * 50

    time_curr = time.time()

    substrings = [genomes[0]]
    substrings.append(longest_common_substring(genomes[1], nitrogenase))

    print time.time() - time_curr
    return substrings

def find_all_substrings_multiprocessed(genomes):
    pool = Pool(num_threads)
    return pool.map(find_all_substrings, genomes)


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    # Highest speed is at 2
    num_threads = 2
    metagenome = load_metagenome()
    nitrogenase = load_nitrogenase_seq()

    time_start = time.time()
    print find_all_substrings_multiprocessed(metagenome[:100])
    print time.time() - time_start
    print "Threads: ", num_threads
