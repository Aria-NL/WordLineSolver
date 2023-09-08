import os
import sys
import json
import string
import random
import time

leftSide = []
rightSide = []
topLetters = []
bottomLetters = []
allLetters = []

# Solver for the New York Times Letter Boxed game
# Takes 4 lists of three letters each, representing the four sides of the box
# Returns the best solution (least words) for the puzzle
# No solution can have less than 2 words
# The words must be at least 3 letters long
# The words must be in the dictionary
# The words must not contain the same letter twice
# The words must not contain the same word twice
# The words cannot contain two consecutive letters from the same side

# Load the words from the dictionary json
def loadWords():
    # Load the words from the dictionary json
    with open('words_dictionary.json', 'r') as f:
        dictionary = list(json.load(f).keys())

    #print first 10 words in the dictionary
    # for i in range(10):
    #     print(dictionary[i])
    return dictionary

def solve():
    # Load the words from the dictionary json
    dictionary = loadWords()

    # Get the letters from the user
    getLetters()

    # Get all the possible words
    words = getAllWords(dictionary)

    # print(words)

    # Get all the possible solutions
    solutions = getAllSolutions(words)
    print(solutions)

    # Get the best solution
    #bestSolution = getBestSolution(solutions)

    # Print the best solution
    #printSolution(bestSolution)

def getLetters():
    global topLetters
    global rightLetters
    global bottomLetters
    global leftLetters
    global allLetters
    # Get the letters from the user
    print("Enter the letters in the box, clockwise from the top left, one side at a time.")
    print("Enter the letters on the top side, separated by spaces.")
    topLetters = input().split()
    print("Enter the letters on the right side, separated by spaces.")
    rightLetters = input().split()
    print("Enter the letters on the bottom side, separated by spaces.")
    bottomLetters = input().split()
    print("Enter the letters on the left side, separated by spaces.")
    leftLetters = input().split()

    allLetters = topLetters + rightLetters + bottomLetters + leftLetters

    if len(allLetters) != 12:
        print("Error: You must enter 12 letters. Ensure you have entered 3 letters for each side.")
        sys.exit()
    for letter in allLetters:
        if len(letter) != 1:
            print("Error: You must enter 12 letters. Ensure you have entered 3 letters for each side.")
            sys.exit()
        if letter.isalpha() == False:
            print("Error: You must enter only letters.")
            sys.exit()
    # if a letter appears twice, exit
    for letter in allLetters:
        if allLetters.count(letter) > 1:
            print("Error: You must enter 12 unique letters.")
            sys.exit()

def getAllWords(dictionary):
    print("Scanning the dictionary for all possible words. This will take a moment.") 
    global topLetters
    global rightLetters
    global bottomLetters
    global leftLetters
    # Get all the possible words
    words = []
    candidateWords = []
    passedLengthCheck = []
    passedWordCheck = []
    passedConsecChecks = []
    passedSideChecks = []
    isBreak = False
    # candidate words begin with any letter from any side
    for letter in allLetters:
        for word in dictionary:
            if word.startswith(letter):
                candidateWords.append(word)
                # print("found candidate " + word)

    # pick 10 random words from the candidate words and print
    # for i in range(10):
    #     randomWord = random.choice(candidateWords)
    #     print(randomWord)


    # slowly filter out words that don't meet the criteria
    # eliminate words that are too short
    for word in candidateWords:
        if len(word) >= 3:
            passedLengthCheck.append(word)
        # else:
            # print("removed " + word + ", too short")
    # iterate through the candidate words letter by letter. if a letter is not in the box, remove the word
    for word in passedLengthCheck:
        isBreak = False
        for letter in word:
            if letter not in allLetters:
                # print("removed " + word + ", letter " + letter + " not in box")
                isBreak = True
                break
        if isBreak:
            continue
        # print("word " + word + " passed letter check")
        passedWordCheck.append(word)
    # eliminate words that contain the same letter twice consecutively
    for word in passedWordCheck:
        isBreak = False
        for i in range(len(word)-1):
            if word[i] == word[i+1]:
                # print("removed " + word + ", same letter twice consecutively")
                isBreak = True
                break
        if isBreak:
            continue
        # print("word " + word + " passed consecutive letter check")
        passedConsecChecks.append(word)
    # remove words that have two consecutive letters from the same side
    for word in passedConsecChecks:
        isBreak = False
        for i in range(len(word)-1):
            if word[i] in topLetters and word[i+1] in topLetters:
                # print("removed " + word + ", two consecutive letters from the top side")
                isBreak = True
                break
            if word[i] in rightLetters and word[i+1] in rightLetters:
                # print("removed " + word + ", two consecutive letters from the right side")
                isBreak = True
                break
            if word[i] in bottomLetters and word[i+1] in bottomLetters:
                # print("removed " + word + ", two consecutive letters from the bottom side")
                isBreak = True
                break
            if word[i] in leftLetters and word[i+1] in leftLetters:
                # print("removed " + word + ", two consecutive letters from the left side")
                isBreak = True
                break
        if isBreak:
            continue
        # print("word " + word + " passed side check")
        passedSideChecks.append(word)
    return passedSideChecks

def getAllSolutions(words):
    validSolutions = []
    # total_combinations = len(words) * len(words)
    progress = 0
    for i in range(len(words)):
        for j in range(len(words)):
            if i != j and words[i][-1] == words[j][0]:
                solution = words[i] + " " + words[j]
                if solution not in validSolutions and len(solution.split()) == 2:
                    if all(letter in solution for letter in allLetters):
                        validSolutions.append(solution)
                # progress += 1
                # print(f"Progress: {progress}/{total_combinations} [{progress/total_combinations*100:.2f}%]", end="\r")
    return validSolutions



solve()