# Copyright 2022 vscode
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
import sys
import re


def load_file() -> List[str]:
    """ load a list of word from a text file"""
    mainlist: List[str] = []
    with open('wordle_nyt_answers.txt') as file:
        mainlist = [line.strip('\n\r') for line in file]

    return mainlist


def count_occurence(words: List[str]) -> None:
    """ count letter occurrence from the words list """

    from collections import Counter

    dicts: List = []

    for word in words:
        count = dict(Counter(word))
        dicts.append(count)

    result = {
        k: [d.get(k) for d in dicts]
        for k in set().union(*dicts)
    }

    for item in result:
        temp = [i for i in result[item] if i is not None]
        print(item, '->', sum(temp))


def run_regexp(pattern: str, words: List[str]) -> List[str]:
    """ run regexp against the list of input words"""

    reg = re.compile(pattern)
    result = list(filter(reg.match, words))
    return result


def search_for_word() -> None:
    """ infinite loop to cascade multiple searchs"""

    words: List[str] = load_file()

    while True:
        command: str = str(input('>'))
        args = [arg for arg in command.split(' ') if arg != ""]

        whatwewant: str = str(args[0])
        result: List[str] = []
        print(f"ok let's try to do that => {whatwewant}")

        if whatwewant == "reset":
            words = load_file()
        elif whatwewant == "exit":
            print("bye bye... see you soon")
            sys.exit()
        elif whatwewant == "exclude":
            exclude: str = str(args[1])
            print(f"exclude: {exclude}")
            exp: str = f"^((?![a-z]*[{exclude}])[a-z])*$"
            result = run_regexp(exp, words)
        elif whatwewant == "include":
            include: str = str(args[1])
            print(f"include: {include}")
            exp: str = "^"
            for char in include:
                exp = exp + f"(?=.*{char})"
            exp = exp + ".*"
            print(exp)
            result = run_regexp(exp, words)
        elif whatwewant == "start":
            startwith: str = str(args[1])
            print(f"start with: {startwith}")
            exp: str = f"^{startwith}.*$"
            result = run_regexp(exp, words)
        elif whatwewant == "end":
            endwith: str = str(args[1])
            print(f"end with: {endwith}")
            exp: str = f"^.*{endwith}$"
            result = run_regexp(exp, words)
        elif whatwewant == "display":
            print(words)
        elif whatwewant == 'count':
            count_occurence(words)
        else:
            result = run_regexp(args[0], words)

        if len(result) == 0:
            print("Sorry nothing found... try again")
        else:
            print(result)
            print(f"found {len(result)} matching word(s) over {len(words)}")
            words = result


if __name__ == "__main__":
    print("let's start!")
    search_for_word()
