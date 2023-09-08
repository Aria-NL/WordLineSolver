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
turns = 0

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
    for i in range(10):
        print(dictionary[i])
    return dictionary

def solve():
    # Load the words from the dictionary json
    dictionary = loadWords()

    # Get the letters from the user
    getLetters()

    # Get all the possible words
    words = getAllWords(dictionary)

    print(words)

    # Get all the possible solutions
    solutions = getAllSolutions(words)
    print(solutions)

    # Get the best solution
    #bestSolution = getBestSolution(solutions)

    # Print the best solution
    #printSolution(bestSolution)

def getLetters():
    global turns
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
    print(allLetters)
    print("Enter the number of words allowed in the solution.")
    turns = int(input())

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
                print("found candidate " + word)

    # pick 10 random words from the candidate words and print
    for i in range(10):
        randomWord = random.choice(candidateWords)
        print(randomWord)


    # slowly filter out words that don't meet the criteria
    # eliminate words that are too short
    for word in candidateWords:
        if len(word) >= 3:
            passedLengthCheck.append(word)
        else:
            print("removed " + word + ", too short")
    # iterate through the candidate words letter by letter. if a letter is not in the box, remove the word
    for word in passedLengthCheck:
        isBreak = False
        for letter in word:
            if letter not in allLetters:
                print("removed " + word + ", letter " + letter + " not in box")
                isBreak = True
                break
        if isBreak:
            continue
        print("word " + word + " passed letter check")
        passedWordCheck.append(word)
    # eliminate words that contain the same letter twice consecutively
    for word in passedWordCheck:
        isBreak = False
        for i in range(len(word)-1):
            if word[i] == word[i+1]:
                print("removed " + word + ", same letter twice consecutively")
                isBreak = True
                break
        if isBreak:
            continue
        print("word " + word + " passed consecutive letter check")
        passedConsecChecks.append(word)
    # remove words that have two consecutive letters from the same side
    for word in passedConsecChecks:
        isBreak = False
        for i in range(len(word)-1):
            if word[i] in topLetters and word[i+1] in topLetters:
                print("removed " + word + ", two consecutive letters from the top side")
                isBreak = True
                break
            if word[i] in rightLetters and word[i+1] in rightLetters:
                print("removed " + word + ", two consecutive letters from the right side")
                isBreak = True
                break
            if word[i] in bottomLetters and word[i+1] in bottomLetters:
                print("removed " + word + ", two consecutive letters from the bottom side")
                isBreak = True
                break
            if word[i] in leftLetters and word[i+1] in leftLetters:
                print("removed " + word + ", two consecutive letters from the left side")
                isBreak = True
                break
        if isBreak:
            continue
        print("word " + word + " passed side check")
        passedSideChecks.append(word)
    return passedSideChecks

def getAllSolutions(words):
    # recursively find all solutions using number of turns.
    # nth word must begin with the last letter of the (n-1)th word
    # the first word can begin with any letter from any side
    def findSolutions(turns, currentWord, usedWords, usedLetters, counter):
        # Base case: we've used all the words
        if turns == 0:
            return [usedWords]

        # Recursive case: try to find the next word
        solutions = []
        for word in words:
            # Check if we've already used this word
            if word in usedWords:
                # print(f"Already used word {word}")
                continue

            # Check if the first letter of this word matches the last letter of the previous word
            if currentWord is not None and word[0] != currentWord[-1]:
                # print("First letter of " + word + " does not match last letter of " + currentWord)
                continue

            # Try using this word
            newUsedWords = usedWords + [word]
            newUsedLetters = usedLetters + list(word)
            newCurrentWord = word
            newTurns = turns - 1

            # Increment the counter and calculate the percentage of completion
            counter += 1
            percent_complete = int(counter / total_iterations * 100)

            # Print the progress indicator
            print(f"\rProgress: {percent_complete}%. Current beginning word: {usedWords[0]} ({'->'.join(usedWords[1:])})", end="")

            # Recursively find the rest of the solutions
            solutions += findSolutions(newTurns, newCurrentWord, newUsedWords, newUsedLetters, counter)

        return solutions

    # Calculate the total number of iterations
    total_iterations = len(allLetters) * (turns - 1) * len(words) ** (turns - 1)

    # Start with all possible first letters
    solutions = []
    counter = 0
    for i, letter in enumerate(allLetters):
        for j in range(2, turns):
            # Calculate the current position of the first word in the list of words
            current_position = i * len(words) + 1
            # Calculate the percentage of completion based on the current position of the first word
            percent_complete = int(current_position / (len(allLetters) * len(words)) * 100)

            # Print the progress indicator before starting a new iteration
            print(f"\rProgress: {percent_complete}%. Current beginning word: {letter} ({'->'.join(['']*j)})", end="")

            solutions += findSolutions(j, letter, [letter], [letter], counter)
            counter += len(words) ** (j - 1)

    # Print the progress indicator when all iterations are complete
    print("\rProgress: 100%. Current beginning word: None")

    return solutions



solve()