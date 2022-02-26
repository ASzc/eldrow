#!/usr/bin/env python3

#
# eldrow, a solver for Wordle puzzles
# Copyright (C) 2022 Alex Szczuczko
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import argparse
import os
import os.path
import string
import sys

#
# Wordlist Prep
#

def read_wordlist(words: list[str]):
    # Determine columns/length
    columns = len(words[0])
    for word in words:
        assert len(word) == columns, "Wordlist does not have a consistent word length"

    # Sort by column/letter coincidence index.
    # First pass: count how many times a letter appears in each column
    # throughout all the words
    letter_appears = { l: [0] * columns for l in string.ascii_lowercase }
    for word in words:
        for column, letter in enumerate(word):
            letter_appears[letter][column] += 1
    #import pprint
    #pprint.pprint(letter_appears)

    # Second pass: for each word, use the predetermined counts on each column
    # to sum a coincidence index
    scores = list()
    for word in words:
        score = sum( letter_appears[l][c] for c, l in enumerate(word) )
        scores.append(score)

    # Sort word list by coincidence index
    words_and_scores = zip(words, scores)
    sorted_words_and_scores = sorted(words_and_scores, key=lambda ws: ws[1], reverse=True)
    sorted_words = list(zip(*sorted_words_and_scores))[0]

    scores_by_word = { w: s for w, s in sorted_words_and_scores }

    return sorted_words, scores_by_word

#
# Solver
#

def parse_known_positions(raw: str) -> list[str]:
    return list(i if i.isalpha() else None for i in raw)

def suggest_words(wordlist: list[str], contains_letters: str, uncontained_letters: str, known_positions: str, known_non_positions: str) -> list[str]:
    contained = set(contains_letters)
    uncontained = set(uncontained_letters)
    known = parse_known_positions(known_positions)
    known_not = parse_known_positions(known_non_positions)

    # Ensure (un)contained has the letters from known as well
    assert len(wordlist[0]) == len(known), "Known positions does not have the same length as the wordlist's words"
    for k in known:
        if k:
            contained.add(k)

    # Ensure uncontained is consistent with contained (contained takes
    # priority)
    uncontained = uncontained.difference(contained)

    # Precalculate booleans for parameter filters
    any_contained = bool(contained)
    any_uncontained = bool(uncontained)
    any_known = any(known)
    any_known_not = any(known_not)

    # Apply all the parameters as filters on the wordlist
    narrow = []
    for word in wordlist:
        characters = set(word)

        copy = True
        if any_contained and not contained.issubset(characters):
            # Example:
            # contained = {"a"}
            # characters = {"a", "b", "o", "r", "t"}
            # -> yes copy, test next parameter
            #
            # Example:
            # contained = {"x"}
            # characters = {"a", "b", "o", "r", "t"}
            # -> no copy
            copy = False
        elif any_uncontained and not uncontained.isdisjoint(characters):
            # Example:
            # uncontained = {"a"}
            # characters = {"a", "b", "o", "r", "t"}
            # -> no copy
            #
            # Example:
            # uncontained = {"x"}
            # characters = {"a", "b", "o", "r", "t"}
            # -> yes copy, test next parameter
            copy = False
        elif any_known and any( k != w for k, w in zip(known, word) if k):
            #for k, w in zip(known, word):
            #    if k and k != w:
            #        return False
            copy = False
        elif any_known_not and any( k == w for k, w in zip(known_not, word) if k):
            copy = False

        if copy:
            narrow.append(word)

    return narrow

#
# Main
#

def arg_parser():
    parser = argparse.ArgumentParser(
        description="Given the state of a Wordle game, and a wordlist, suggest one or more possible solutions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-o", "--output", help="Write the suggested word(s) to a file instead of stdout")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Change the default maximum number of suggested words")
    parser.add_argument("-s", "--show-score", action="store_true", help="Show the coincidence score alongside each suggested word")
    parser.add_argument("-w", "--wordlist", default="wordlist.txt", help="Change the default path of the wordlist file")
    parser.add_argument("-p", "--present", default="", help="Specify any letters that are known to exist somewhere in the word. Order doesn't matter.")
    parser.add_argument("-n", "--not-present", default="", help="Specify any letters that are known to not exist anywhere in the word. Any letters specified in the list of present letters will override letters specified here. Order doesn't matter.")
    parser.add_argument("-k", "--known-positions", default=".....", help="Specify any positions/columns that are known to contain a particular letter. Use a period character (or any other non-letter) to specify unknown positions. Any letters specified here will also be added to the list of present letters. Must be the same length as the words in the wordlist. Examples: a..ot .b... ....s")
    parser.add_argument("-i", "--known-non-positions", default=".....", help="Specify any positions/columns that are known to NOT contain a particular letter. Same syntax as --known-positions")

    return parser

def main(raw_args):
    parser = arg_parser()
    args = parser.parse_args(raw_args)

    # Read wordlist, ignoring whitespace, and normalizing case
    with open(args.wordlist, "r") as f:
        lines = ( line.strip() for line in f )
        raw_wordlist = list( line.lower() for line in lines if line )
    # Parse it
    wordlist, scores_by_word = read_wordlist(raw_wordlist)

    # Generate all suggestions
    suggestions = suggest_words(wordlist, args.present, args.not_present, args.known_positions, args.known_non_positions)

    # Determine zero padding requirements
    if suggestions:
        zpad = max( len(str(score)) for score in ( scores_by_word[suggestion] for suggestion in suggestions ) )

    # Write a portion of these suggestions to the output
    def write(f):
        for i, suggestion in enumerate(suggestions):
            if i >= args.limit:
                break
            if args.show_score:
                f.write(str(scores_by_word[suggestion]).zfill(zpad))
                f.write(" ")
            f.write(suggestion)
            f.write("\n")
    if args.output:
        with open(args.output, "w") as f:
            write(f)
    else:
        write(sys.stdout)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
