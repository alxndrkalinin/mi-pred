#!/usr/bin/python

import sys
import os

def comple(ch):
        if ch == 'A':
                return 'T'
        elif ch == 'T':
                return 'A'
        elif ch == 'G':
                return 'C'
        elif ch == 'C':
                return 'G'

def complement(seq):
        return ''.join(map(comple, seq))

def init_matrix(row, column):
        return [[0 for _ in range(column)] for _ in range(row)]

def print_matrix(matrix):
        for i in range(0, len(matrix)):
                for j in range(0, len(matrix[0])):
                        print("%s " % matrix[i][j])
                print("\n")

def score(nuc1, nuc2):
        if nuc1 == nuc2:
                return 5
        elif (nuc1 == 'G' and nuc2 == 'A') or (nuc1 == 'C' and nuc2 == 'T'):
                return 2
        else:
                return -4

def align_score(seq1, seq2):
        len1 = len(seq1)
        len2 = len(seq2)
        max_scr = 0
        S = init_matrix(len1 + 1, len2 + 1)
        for i in range(1, len1 + 1):
                for j in range(1, len2 + 1):
                        scr = score(seq1[i - 1], seq2[j - 1])
                        align = S[i - 1][j - 1] + scr
                        gap1 = S[i - 1][j] - 8  # Gap penalty
                        gap2 = S[i][j - 1] - 8  # Gap penalty
                        S[i][j] = max(align, gap1, gap2, 0)
                        if S[i][j] > max_scr:
                                max_scr = S[i][j]
        return max_scr

f1 = open(sys.argv[1])
for line1 in f1:
        if line1[0] == '>':
                anno1 = line1
        else:
                seq1 = complement(line1.strip())[::-1]
                print('seq1: ' + seq1)
                f2 = open(sys.argv[2])
                for line2 in f2:
                        if line2[0] == '>':
                                anno2 = line2
                        else:
                                seq2 = line2.strip()
                                print('seq2: ' + seq2)
                                print(anno1.strip() + ' ' + anno2.strip())
                                print(align_score(seq1, seq2))
                                print
                f2.close()
f1.close()
