#!/usr/bin/env python3
"""TDDE44, lab7."""

import sys
from med import minimum_edit_distance
from time import time


def Main(frequency, texts):
    """Läser av frequency filen och gör om det till en lista."""
    timer = time()
    TXT = "Nummberr of Files that are gonna be controlled: {}"
    print(TXT.format(len(texts)))
    file = open(frequency, encoding="utf-8")
    frequency_data = []
    for row in file:
        row = row.rstrip().split("\t")
        frequency_data.append(row)
    TXT2 = "Loading word frequency data from :{}. \n\
    Frequency data for: {} words loaded."
    print(TXT2.format(frequency, len(frequency_data)))
    file.close()
    for argument in texts:
        Report(frequency_data, argument, timer)


class Report(object):
    """Skapar filerna med felstavade ord och tre förslag för dem."""

    def __init__(self, frequency_data, text_to_check, timer):
        """Instanser av klassen Report skapas."""
        self.warninglist = []
        self.text_file = self.fileloader(text_to_check)
        TXT1 = "File that are gonna be contrlled: {}: "
        print(TXT1.format(text_to_check))
        line = 0
        for row in self.text_file:
            line += 1
            for word in row:
                if self.word_in_freq(word, frequency_data) is False:
                    instance = SpellingWarning(word, frequency_data)
                    insatce1 = instance.word_error
                    self.warninglist.append(
                        (line, insatce1, instance.word_to_suggest))

        TXT2 = "Found {} unknown words."
        print(TXT2.format(len(self.warninglist)))
        self.print_report(text_to_check, round(time() - timer, 2))

    def fileloader(self, text_to_check):
        """Texter som skickas in läsas av och en lista av meningar skickas."""
        self.text_to_check = text_to_check
        file = open(self.text_to_check, 'r', encoding="utf-8")
        text = file.read().replace('.', "").lower()
        text = ''.join(c for c in text if c.isalpha()
                       or c in '\n' or c in ' ' or '')
        row_list = text.split("\n")

        Final_list = []
        for index in row_list:

            word_list = index.split(" ")

            for word in word_list:
                if word in ("", " ", "-"):
                    word_list.remove(word)
            Final_list.append(word_list)
        return Final_list

    def word_in_freq(self, word, frequency_list):
        """Returnera True om word finns i frequency_list."""
        for word_freq in frequency_list:
            if word_freq[0] == word:
                return True
        return False

    def print_report(self, textfile, run_time):
        """Skapa textfil och information skrivs in i den."""
        report = open("Report-" + textfile, "w")

        TXT = "saving repport to '{}' "
        print(TXT.format(str("Report " + textfile)))
        report.write("Spell check for  '{}' took {} sekunder.\n".format(
            textfile, run_time))
        for index in self.warninglist:

            report.write("[line {}], {}: {}, {}, {}.\n".format(
                index[0], index[1], index[2][0], index[2][1], index[2][2]))


class SpellingWarning(object):
    """Går igenom frequency_list och hittar tre förslag."""

    def __init__(self, word_error, frequency_list):
        """Instanser till klassen Spellningswarning defineras."""
        self.word_error = word_error
        self.word_to_suggest = self.suggest(frequency_list)

    def suggest(self, frequency_list):
        """Ta fram 3 förslag på rättstavning."""
        word_suggestions = {}
        for word in frequency_list[0:10000]:
            if len(word_suggestions) < 3:
                word_suggestions[word[0]] = minimum_edit_distance(
                    self.word_error, word[0])

            key_max = max(word_suggestions, key=word_suggestions.get)

            if word_suggestions[key_max] > minimum_edit_distance(
                    self.word_error, word[0]):

                del(word_suggestions[key_max])

                word_suggestions[word[0]] = minimum_edit_distance(
                    self.word_error, word[0])
        word_suggestions = list(word_suggestions.keys())
        return (word_suggestions)


if __name__ == "__main__":
    Main(sys.argv[1], sys.argv[2:])
