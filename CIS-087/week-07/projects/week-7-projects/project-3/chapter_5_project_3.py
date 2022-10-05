"""
Program: generator.py
Author: Ken
Generates and displays sentences using a simple grammar
and vocabulary.  Words are chosen at random.

Modified By:    Jeff Alkire
Date:           October 5, 2022
Purpose:        Complete project 3 from chapter 5 in text.
"""

import random

def get_words(filename: str):  # returns tuple of unknown length - all strings.
    """
    Get a list of words from a file.  The file should contain one word on a line
        with no whitespace other than the new lines.
    :param filename: Name of the file to process
    :return:  a tuple with one entry for each line in the supplied file
    """
    with open(filename) as f:
        results = f.readlines()

    stripped_results = []
    for s in results:
        stripped_str = s.strip()
        if "" != stripped_str:
            stripped_results.append( s.strip() )

    return tuple(stripped_results)

# read words to use from disk.
articles = get_words("articles.txt")
nouns = get_words("nouns.txt")
verbs = get_words("verbs.txt")
prepositions = get_words("prepositions.txt")


def sentence():
    """Builds and returns a sentence."""
    return nounPhrase() + " " + verbPhrase()

def nounPhrase():
    """Builds and returns a noun phrase."""
    return random.choice(articles) + " " + random.choice(nouns)

def verbPhrase():
    """Builds and returns a verb phrase."""
    return random.choice(verbs) + " " + nounPhrase() + " " + \
           prepositionalPhrase()

def prepositionalPhrase():
    """Builds and returns a prepositional phrase."""
    return random.choice(prepositions) + " " + nounPhrase()

def main():
    """Allows the user to input the number of sentences
    to generate."""
    number = int(input("Enter the number of sentences: "))
    for count in range(number):
        print(sentence())

# The entry point for program execution
if __name__ == "__main__":
    main()
