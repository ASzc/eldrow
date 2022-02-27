# Eldrow

A solver for Wordle puzzles. Suggests words for you to use, based on the current state of the game that you input, and a wordlist.

## Usage

### game

```
usage: eldrow.py game [-h] [-o OUTPUT] [-l LIMIT] [-s] [-w WORDLIST]
                      [MOVE RESPONSE ...]

Given a wordlist, and zero or more previous moves and responses, suggest one
or more possible solutions

positional arguments:
  MOVE RESPONSE         A move followed by the response from Wordle. There
                        should be an even number of arguments. Use y for
                        yellow, g for green, b for black. Ex: abort ygbbb

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Write the suggested word(s) to a file instead of
                        stdout
  -l LIMIT, --limit LIMIT
                        Change the default maximum number of suggested words
  -s, --show-score      Show the coincidence score alongside each suggested
                        word
  -w WORDLIST, --wordlist WORDLIST
                        Change the default path of the wordlist file
```

### suggest

```
usage: eldrow.py suggest [-h] [-o OUTPUT] [-l LIMIT] [-s] [-w WORDLIST]
                         [-p PRESENT] [-n NOT_PRESENT] [-k KNOWN_POSITIONS]
                         [-i KNOWN_NON_POSITIONS]

Given the state of a Wordle game, and a wordlist, suggest one or more possible
solutions

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Write the suggested word(s) to a file instead of
                        stdout
  -l LIMIT, --limit LIMIT
                        Change the default maximum number of suggested words
  -s, --show-score      Show the coincidence score alongside each suggested
                        word
  -w WORDLIST, --wordlist WORDLIST
                        Change the default path of the wordlist file
  -p PRESENT, --present PRESENT
                        Specify any letters that are known to exist somewhere
                        in the word. Order doesn't matter.
  -n NOT_PRESENT, --not-present NOT_PRESENT
                        Specify any letters that are known to not exist
                        anywhere in the word. Any letters specified in the
                        list of present letters will override letters
                        specified here. Order doesn't matter.
  -k KNOWN_POSITIONS, --known-positions KNOWN_POSITIONS
                        Specify any positions/columns that are known to
                        contain a particular letter. Use a period character
                        (or any other non-letter) to specify unknown
                        positions. Any letters specified here will also be
                        added to the list of present letters. Must be the same
                        length as the words in the wordlist. Examples: a..ot
                        .b... ....s
  -i KNOWN_NON_POSITIONS, --known-non-positions KNOWN_NON_POSITIONS
                        Specify any positions/columns that are known to NOT
                        contain a particular letter. Multiple overlapping
                        patterns can be entered via sequential uses of this
                        argument. Same syntax as --known-positions
```

### compare

```
usage: eldrow.py compare [-h] target guess

Given a target word and a guess, print Wordle YGB syntax

positional arguments:
  target      Word that is the target
  guess       An attempt at guessing the target word. Must be the same length
              as the target word

options:
  -h, --help  show this help message and exit
```

### complete

```
usage: eldrow.py complete [-h] [-w WORDLIST] [-o OUTPUT]

Check the completeness of eldrow's solving ability against the wordlist

options:
  -h, --help            show this help message and exit
  -w WORDLIST, --wordlist WORDLIST
                        Change the default path of the wordlist file
  -o OUTPUT, --output OUTPUT
                        Write a report to this file
```

## Generating word lists

### Official

The official wordlists can be extracted from the javascript source code available from the wordle page. There is one for valid answers, and one for all accepted input words. See `official-answer-wordlist.txt` and `official-support-wordlist.txt`.

### General Purpose

There are many wordlists available on the internet. To make a general purpose wordlist work for Wordle, you need to narrow the number of letters to exactly 5. This is easily done with grep:

```
grep '^.....$' raw/twl06.txt > wordlist.txt
```

Eldrow is capable of handling other lengths than 5, if desired. You must generate a wordlist to match, and set the `-k` option with an appropriate number of periods.

## License

This software is available under the AGPL v3. See the license header in the source code for details.
