"""
convertNumbers.py
@author: Carlos Antonio Heinze Mortera A01700179
A tool to convert integers from a file into binary and hexadecimal
formats.
"""

import sys
import time


def to_binary(number):
    """
    Converts an integer to a 32-bit binary string.

    Args:
        number (int): The integer to convert.

    Returns:
        str: The 24-bit binary string to match results txt
    """
    # Handle Two's Complement for 32 bits
    if number < 0:
        number = (1 << 32) + number
    elif number == 0:
        return "0".zfill(32)

    bits = ""
    temp_num = number
    while temp_num > 0:
        remainder = temp_num % 2
        bits = str(remainder) + bits
        temp_num = temp_num // 2

    if len(bits) > 32:
        bits = bits[-32:]
    return bits[:24]


def to_hexadecimal(number):
    """
    Converts an integer to a 32-bit hexadecimal string.

    Args:
        number (int): The integer to convert.

    Returns:
        str: The hexadecimal string.
    """
    hex_chars = "0123456789ABCDEF"

    hex_str = ""
    temp_num = number
    while temp_num > 0:
        remainder = temp_num % 16
        hex_str = hex_chars[remainder] + hex_str
        temp_num = temp_num // 16

    if len(hex_str) > 8:
        hex_str = hex_str[-8:]
    return hex_str


def convert_number(int_num):
    """
    Converts an integer to binary and hex representations

    Args:
        int_number (int): The integer to convert.

    Returns:
        str: The hexadecimal string.
    """
    # Conversion for 2s Complement (negative numbers)
    # Convert for negative, do nothing for positive
    if int_num < 0:
        number = (1 << 32) + int_num
    elif int_num == 0:
        return "0", "0"
    else:
        number = int_num

    hexadecimal_representation = to_hexadecimal(number)
    binary_representation = to_binary(number)

    return binary_representation, hexadecimal_representation


def main():
    """Main execution function for the number converter."""
    start_time = time.time()

    if len(sys.argv) < 2:
        print("Error use command: python convertNumbers.py <fileWithData.txt>")
        return

    input_file = sys.argv[1]

    try:
        with open("ConvertionResults.txt", 'w', encoding='utf-8') as out_file:
            print(f"{'INDEX':<6} | {'NUMBER':<12} |"
                  f"{'BINARY':<10} | {'HEX':<10}")
            print("-" * 50)
            out_file.write(f"{'INDEX':<6} | {'NUMBER':<12} |"
                           f"{'BINARY':<10} | {'HEX':<10}\n")
            out_file.write("-" * 50 + "\n")

            with open(input_file, 'r', encoding='utf-8') as in_file:
                index = 1
                for line in in_file:
                    clean_line = line.strip()
                    if not clean_line:
                        continue
                    try:
                        # Cast to integer
                        val = int(clean_line)
                        bin_val, hex_val = convert_number(val)

                        # Print the result and write it to the output file
                        row = f"{index:<6} | {val:<12} |" \
                              f"{bin_val:24} | {hex_val:<10}"
                        print(row)
                        out_file.write(row + "\n")
                        index += 1
                    except ValueError:
                        print(f"Error: Invalid data skipped: \
                               '{clean_line}'")
                        bin_val = "#!VALUE"
                        hex_val = "#!VALUE"
                        row = f"{index:<6} | {clean_line:<12} |" \
                              f"{bin_val:24} | {hex_val:<10}"
                        print(row)
                        out_file.write(row + "\n")
                        index += 1

            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"Elapsed Time: {elapsed_time:.4f} seconds")
            out_file.write(f"Elapsed Time: {elapsed_time:.4f} seconds")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except IOError as e:
        print(f"Error writing to file: {e}")


if __name__ == "__main__":
    main()
