# -*- coding: utf-8 -*-
"""
Mini Project 1: Gene Finder

@author: Adam Novotny

"""

import random
from amino_acids import aa, codons, aa_table   # you may find these useful
from load import load_seq

stop_codons = 10
start_codon = 3


def shuffle_string(s):
    """Shuffles the characters in the input string
        NOTE: this is a helper function, you do not
        have to modify this in any way """
    return ''.join(random.sample(s, len(s)))

# YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    >>> get_complement('t')
    'A'
    """
    nucleotideList = ['A', 'C', 'T', 'G']
    return nucleotideList[(nucleotideList.index(nucleotide.upper()) + 2) % 4]

    # if(nucleotide == 'A'):
    #     return 'T'
    # elif(nucleotide == 'T'):
    #     return 'A'
    # elif(nucleotide == 'C'):
    #     return 'G'
    # elif(nucleotide == 'G'):
    #     return 'C'
    # else:
    #     raise ValueError("get_complement() only accepts ['A','T','C','G'] as input. You input '" + nucleotide + "'.")


def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence

        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    reverseDNA = ""
    for i in reversed(dna):
        reverseDNA += get_complement(i)

    return reverseDNA


def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start
        codon and returns the sequence up to but not including the
        first in frame stop codon.  If there is no in frame stop codon,
        returns the whole string.

        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    >>> rest_of_ORF("Rekd")
    Traceback (most recent call last):
        ...
    ValueError: Sequence must begin with ATG.
    """

    if(dna[:3].upper() not in codons[start_codon]):
        raise ValueError("Sequence must begin with ATG.")

    for i in range(int(len(dna) / 3)):
        if(dna[i*3:(i+1)*3] in codons[stop_codons]):
            return dna[:i*3]

    return dna


def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA
        sequence and returns them as a list.  This function should
        only find ORFs that are in the default frame of the sequence
        (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.

        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGGGGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    >>> find_all_ORFs_oneframe("CATGAATGTAGATAGATGTGCCC")
    ['ATGTGCCC']
    >>> find_all_ORFs_oneframe("CATGAATGTAGAATGATGTGCCC")
    ['ATGATGTGCCC']
    """

    orfs = []

    i = 0
    while(i < len(dna)):
        # print(i, dna[i:])
        if(dna[i:(i+3)] in codons[start_codon]):
            # print("Found codon at ", i*3, dna[i*3:])
            orfs.append(rest_of_ORF(dna[i:]))
            # print("Found codon", orfs[-1])
            # print("i is at", i, ". Skipping ahead", len(orfs[-1]))
            i += len(orfs[-1])
        else:
            i += 3

    return orfs


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in
        all 3 possible frames and returns them as a list.  By non-nested we
        mean that if an ORF occurs entirely within another ORF and they are
        both in the same frame, it should not be included in the returned list
        of ORFs.

        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    orfs = []

    for i in range(3):
        orfs = orfs + find_all_ORFs_oneframe(dna[i:])

    return orfs


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.

        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """

    orfs = find_all_ORFs(dna)
    orfs = orfs + find_all_ORFs(get_reverse_complement(dna))

    return orfs

#
#
# def longest_ORF(dna):
#     """ Finds the longest ORF on both strands of the specified DNA and returns it
#         as a string
#     >>> longest_ORF("ATGCGAATGTAGCATCAAA")
#     'ATGCTACATTCGCAT'
#     """
#     # TODO: implement this
#     pass
#
#
# def longest_ORF_noncoding(dna, num_trials):
#     """ Computes the maximum length of the longest ORF over num_trials shuffles
#         of the specfied DNA sequence
#
#         dna: a DNA sequence
#         num_trials: the number of random shuffles
#         returns: the maximum length longest ORF """
#     # TODO: implement this
#     pass
#
#
# def coding_strand_to_AA(dna):
#     """ Computes the Protein encoded by a sequence of DNA.  This function
#         does not check for start and stop codons (it assumes that the input
#         DNA sequence represents an protein coding region).
#
#         dna: a DNA sequence represented as a string
#         returns: a string containing the sequence of amino acids encoded by the
#                  the input DNA fragment
#
#         >>> coding_strand_to_AA("ATGCGA")
#         'MR'
#         >>> coding_strand_to_AA("ATGCCCGCTTT")
#         'MPA'
#     """
#     # TODO: implement this
#     pass
#
#
# def gene_finder(dna):
#     """ Returns the amino acid sequences that are likely coded by the specified dna
#
#         dna: a DNA sequence
#         returns: a list of all amino acid sequences coded by the sequence dna.
#     """
#     # TODO: implement this
#     pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
