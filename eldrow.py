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
import sys

#
# Wordlist Prep
#

def read_wordlist(words: list[str]) -> dict:
    wordlist = dict()

    # Determine columns/length
    # TODO

    # Sort by column/letter coincidence index
    # TODO


    return wordlist

#
# Solver
#

def parse_known_positions(raw: str) -> list[str]:
    return list(i if i.isalpha() else None for i in raw)

def suggest_words(wordlist: dict, contains_letters: str, uncontained_letters: str, known_positions: str) -> list[str]:
    contained = set(contains_letters)
    uncontained = set(uncontained_letters)
    known = parse_known_positions(known_positions)

    # Ensure contained has the letters from known as well
    assert wordlist["columns"] == len(known)
    for k in known:
        if k:
            contained.add(k)

    # TODO

    return suggestions

#
# Main
#

def file_exists(parser, arg):
    if not os.path.exists(arg):
        parser.error(f"The file {arg} does not exist!")
    else:
        return arg

def arg_parser():
    parser = argparse.ArgumentParser(
        description="Given the state of a Wordle game, and a wordlist, suggest one or more possible solutions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-o", "--output", help="Write the suggested word(s) to a file instead of stdout")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Change the default maximum number of suggested words")
    parser.add_argument("-w", "--wordlist", type=file_exists, default="wordlist.txt", help="Change the default path of the wordlist file")
    parser.add_argument("-p", "--present", default="", help="Specify any letters that are known to exist somewhere in the word. Order doesn't matter.")
    parser.add_argument("-n", "--not-present", default="", help="Specify any letters that are known to not exist anywhere in the word. Order doesn't matter.")
    parser.add_argument("-k", "--known-positions", default=".....", help="Specify any positions/columns that are known to contain a particular letter. Use a period character (or any other non-letter) to specify unknown positions. Any letters specified here will also be added to the list of present letters. Must be the same length as the words in the wordlist. Examples: a..ot .b... ....s")

    return parser

def main(raw_args):
    parser = arg_parser()
    args = parser.parse_args(raw_args)

    # Read wordlist, ignoring whitespace
    with open(args.wordlist, "r") as f:
        lines = (line.strip() for line in f)
        raw_wordlist = list(line for line in lines if line)
    # Parse it
    wordlist = read_wordlist(raw_wordlist)

    # Generate all suggestions
    suggestions = suggest_words(wordlist, args.present, args.not_present, args.known_positions)

    # Write a portion of these suggestions to the output
    def write(f):
        for i, suggestion in enumerate(suggestions):
            if i >= args.limit:
                break
            f.write(suggestion)
            f.write("\n")
    if args.output:
        with open(args.output, "w") as f:
            write(f)
    else:
        write(sys.stdout)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
