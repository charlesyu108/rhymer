#!/usr/bin/env python
#
# Charles Yu 
# May 31, 2016
#
# Given a word, this script will print out words that rhyme with the given
# word/pronounciation and phonetic similarity of the rhymed word to the orignal,
# denoted by ascending order of how many phonemes are shared between the two words.
#
# Inspired by https://www.reddit.com/r/dailyprogrammer/comments/4fnz37/20160420_challenge_263_intermediate_help_eminem/
# 
# Phoneme dictionary thanks to the CMU Sphinx project, Copyright disclaimer
# reproduced below:
# =============================================================================
# Copyright (C) 1993-2015 Carnegie Mellon University. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#    The contents of this file are deemed to be source code.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# This work was supported in part by funding from the Defense Advanced
# Research Projects Agency, the Office of Naval Research and the National
# Science Foundation of the United States of America, and by member
# companies of the Carnegie Mellon Sphinx Speech Consortium. We acknowledge
# the contributions of many volunteers to the expansion and improvement of
# this dictionary.
#
# THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
# NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# =============================================================================


#List of vowel phonemes
vowels = ['AA','AE', 'AH', 'AO','AW', 'AY', 'EH', 'ER', 'EY',
          'IH', 'IY', 'OW', 'OY', 'UH','UW']

""" This method takes a String inpt, the word to be rhymed, and returns
the a String: the user's selected prounciation of the word to be rhymed.
Pronouncer exits the program if no words matching inpt are found."""
def pronouncer(inpt):
    inptlen = len(inpt)
    inpt = inpt.upper()
    
    pronounced = []
    
    for line in open('cmusphinx.txt'):
        if line[0:inptlen] == inpt:
            pronounced.append(line)
            
    if len(pronounced) == 0:
        print "Sorry, no matching results found. Please try again."
        exit()
    elif len(pronounced) == 1:
        selection = pronounced[0]
    elif len(pronounced) > 1:
        selection = prouncerhelper(inpt, pronounced)
        
    return selection

"""This is the helper method for prounouncer. It takes a String inpt and a
list of Strings prns and returns a String, the user's desired pronounciation.
The method displays all elements of prns (all the pronounciations of inpt and
all prounciations of words containing inpt) as passed by prouncouncer, and
prompts the user to make a selection for the desired pronounciations. """

def prouncerhelper(inpt,prns):
    n = 0
    for i in prns:
        print "(" + str(n) + "): " + i
        n = n + 1
    print("There is more than one result(s) for " + inpt +", which would you like?")
    try:
        choice = int(raw_input("Please enter the line number of your choice: " ))
        assert choice >= 0 and choice < len(prns)
        selection = prns[choice]
        return selection
        
    except AssertionError or ValueError:
        print("Please enter a valid selection. Try again...")
        exit()

"""Takes a String selection and Returns a list of [String ending, String[] phonemes].
Parses the text of selection and creates a list of phonemes. Identifies the last vowel
in selection and the ending(the part that signifies a rhyme rhymed) """

def getEnding(selection):
    trim = selection[selection.index(" "):]
    trim = trim.strip()
    phonemes = trim.split()
    
    i = len(phonemes) - 1
    lastvowel = None
    while i >= 0:
        for item in vowels:
            if item in phonemes[i]:
                lastvowel = i
                break
            
        if lastvowel is not None:
            break
        
        i = i -1
        
    ending = ' '.join(phonemes[lastvowel:])
    return [ending, phonemes]

"""Takes a list inpt of the format [String ending, String[] phonemes], identifies
rhyming words, sorts words, and prints a display of rhyming words."""

def findRhymes(inpt):
    ending = inpt[0]
    phonemes = inpt[1]
    rev = phonemes[:]
    rev.reverse()
    
    rhyming = []
    for line in open('cmusphinx.txt'):
        if (line.rfind(ending) == len(line) - len(ending) - 1) and ';;;' not in line:
            samePhns = 0
            rline = line.split()
            rline.reverse()
           
            for t in range(0,len(rev)):
                if rline[t] == rev[t]:
                    samePhns = samePhns + 1
                else:
                    break
            rhyming.append([line[:line.index(' ')],samePhns])
            
    if len(rhyming) == 0:
        print ("Sorry! No rhymes found!")
        exit()
        
    else:
        quicksort(rhyming, 0, len(rhyming)-1)
        for item in rhyming:
            print item[0] + ', Number of matching phonemes: [' + str(item[1]) + ']'
        print str(len(rhyming)) + " results in total"
        
        
"""Recursively sorts a rhymeArray input of the form [String ending, String[] phonemes]."""        
def quicksort(rhymeArray,h,k):
    if h < k:
        p = qshelp(rhymeArray,h,k)
        quicksort(rhymeArray, h, p-1)
        quicksort(rhymeArray, p, k)
    
"""Helper function for quicksort. Does the partioning work for the sort.
Takes a list arr of the form [String ending, String[] phonemes], int h
(the beginning index of the portion to be sorted), int k (the end index
of the portion to be sorted) and returns an int of the new pivot index"""
def qshelp(arr,h,k):
    pivot = arr[(h+k)/2][1]
    
    while h <= k:
        while (arr[h][1] < pivot):
            h = h +1
        while (arr[k][1] > pivot):
            k = k - 1
                  
        if (h <=k):
            tmp = arr[h]
            arr[h] = arr[k]
            arr[k] = tmp
            h = h + 1
            k = k -1
    return h
    
     
def main():
    inpt = raw_input('Enter the word to rhyme: ')
    prncd = pronouncer(inpt)
    rhymeinfo = getEnding(prncd)
    findRhymes(rhymeinfo)
    


if __name__ == '__main__':
    main()
    


