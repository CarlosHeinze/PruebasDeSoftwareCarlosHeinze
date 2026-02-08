"""
wordCount.py
@author: Carlos Antonio Heinze Mortera A01700179
Program to count the nomber and frequency of
words in a file
"""

import sys
import time


def remove_whitespaces(word):
    """
    Converts an integer to binary and hex representations

    Args:
        word (str): Word to process.

    Returns:
        clean_word (str): word with no end of line or white characters.
    """
    whitespace = (' ', '\t', '\n', '\r')
    clean_word = ""
    for char in word:
        if char in whitespace:
            break
        clean_word += char
    return clean_word


def process_file(filename):
    """
    Converts an integer to binary and hex representations

    Args:
        filename (str): Filename of the txt to process.

    Returns:
        word_freq (dict): Dictionary with the words and frequencies
        total (int): Total number of words read
    """
    word_freq = {}
    total_words = 0
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for word in file:
                try:
                    word_stripped = remove_whitespaces(word)
                    if word_stripped != "":
                        if word_stripped in word_freq:
                            word_freq[word_stripped] += 1
                        else:
                            word_freq[word_stripped] = 1
                        total_words += 1
                except ValueError:
                    print(f"Error in row: {word_stripped}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        word_freq = {}
    return word_freq, total_words


def sort_dictionary(words):
    """
    Takes a dictionary with words and frequencies, and converts it
    to a list of tuples ordered by frequency. Uses Bubble sort.

    Args:
        filename (str): Filename of the txt to process.

    Returns:
        word_freq (dict): Dictionary with the words and frequencies
    """
    items = []
    for word in words:
        items.append([word, words[word]])

    n = len(items)

    for i in range(n):
        for j in range(0, n - i - 1):
            # Use the second item in the tuple to sort
            if items[j][1] < items[j + 1][1]:
                temp = items[j]
                items[j] = items[j + 1]
                items[j + 1] = temp
    return items


def write_output(word_freq, start_time, total):
    """
    Converts an integer to binary and hex representations

    Args:
        word_freq (dict): Dictionary with the words and frequencies.
        total (int): Total number of words
    """
    try:
        with open("WordCountResults.txt", 'w', encoding='utf-8') as out_file:
            print(f"{'Row Label':<20} | {'Count':<10}")
            print("-" * 33)
            out_file.write(f"{'Row Label':<20} | {'Count':<10}" + "\n")
            out_file.write("-" * 33 + "\n")

            for word, count in sort_dictionary(word_freq):
                line = f"{word:<20} | {count:<10}"
                print(line)
                out_file.write(line + "\n")
            out_file.write(f"Grand Total: {total}\n")
            print(f"Grand Total: {total}")
            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"Elapsed Time: {elapsed_time:.4f} seconds")
            out_file.write(f"Elapsed Time: {elapsed_time:.4f} seconds")

    except IOError as e:
        print(f"Error writing to result file: {e}")


def main():
    """Main execution function for the word counter."""
    start_time = time.time()

    if len(sys.argv) < 2:
        print("Error use command: python wordCount.py <fileWithData.txt>")
        return

    input_file = sys.argv[1]

    words_dict, total = process_file(input_file)
    if not words_dict:
        print("Empty File or error reading")
    else:
        write_output(words_dict, start_time, total)


if __name__ == "__main__":
    main()
