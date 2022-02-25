# Eldrow

A solver for Wordle puzzles. Suggests words for you to use, based on the current state of the game that you input, and a wordlist.

## Usage

```
usage: eldrow.py [-h] [-o OUTPUT] [-l LIMIT] [-s] [-w WORDLIST] [-p PRESENT]
                 [-n NOT_PRESENT] [-k KNOWN_POSITIONS]

Given the state of a Wordle game, and a wordlist, suggest one or more possible
solutions

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Write the suggested word(s) to a file instead of
                        stdout (default: None)
  -l LIMIT, --limit LIMIT
                        Change the default maximum number of suggested words
                        (default: 10)
  -s, --show-score      Show the coincidence score alongside each suggested
                        word (default: False)
  -w WORDLIST, --wordlist WORDLIST
                        Change the default path of the wordlist file (default:
                        wordlist.txt)
  -p PRESENT, --present PRESENT
                        Specify any letters that are known to exist somewhere
                        in the word. Order doesn't matter. (default: )
  -n NOT_PRESENT, --not-present NOT_PRESENT
                        Specify any letters that are known to not exist
                        anywhere in the word. Any letters specified in the
                        list of present letters will override letters
                        specified here. Order doesn't matter. (default: )
  -k KNOWN_POSITIONS, --known-positions KNOWN_POSITIONS
                        Specify any positions/columns that are known to
                        contain a particular letter. Use a period character
                        (or any other non-letter) to specify unknown
                        positions. Any letters specified here will also be
                        added to the list of present letters. Must be the same
                        length as the words in the wordlist. Examples: a..ot
                        .b... ....s (default: .....)
```

## License

This software is available under the AGPL v3. See the license header in the source code for details.
