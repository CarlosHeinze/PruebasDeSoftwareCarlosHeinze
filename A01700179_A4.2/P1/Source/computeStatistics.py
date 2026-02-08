"""
computeStatistics.py
A tool to calculate descriptive statistics from a file.
Compliant with PEP8.
"""

import sys
import time


def calculate_mean(numbers, length):
    """
    Calculates the mean/average of a list of numbers

    Args:
        numbers (list): A list of numbers read from the initial file.
        length (int): Size of the list of numbers.

    Returns:
        mean (float): The average or mean calculated from the numbers list.
    """
    total_sum = 0
    if not numbers:
        mean = 0
    else:
        for num in numbers:
            total_sum = total_sum + num
        mean = total_sum / length
    return mean


def calculate_median(numbers, length):
    """
    Calculates the median value of a unsorted list of numbers.

    Args:
        numbers (list): A list of numbers read from the initial file.
        length (int): Size of the list of numbers.

    Returns:
        median (float): Median of the numbers in the list.
    """
    if not numbers:
        median = 0
    sorted_nums = sorted(numbers)
    mid = length // 2

    if length % 2 == 0:
        median = (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    else:
        median = sorted_nums[mid]
    return median


def calculate_mode(numbers):
    """
    Calculates the mode (most frequent value).

    Args:
        numbers (list): A list of numbers read from the initial file.

    Returns:
        mode (list): A list of the modes in the numbers list.
    """
    if not numbers:
        return None
    counts = {}
    for num in numbers:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1

    max_count = 0
    modes = []
    for num, count in counts.items():
        if count > max_count:
            max_count = count
            modes = []
            modes.append(num)
        elif count == max_count:
            modes.append(num)

    return modes


def calculate_variance(numbers, mean, length):
    """
    Calculates the variance of the list of numbers.

    Args:
        numbers (list): A list of numbers read from the initial file.
        length (int): Size of the list of numbers.

    Returns:
        variance (float): The population variance calculated.
    """
    if not numbers:
        variance = 0
    sum_sq_diff = sum((x - mean) ** 2 for x in numbers)

    # Nota: Use el calculo poblacional ya que asi vienen las instrucciones
    # aunque los resultados muestren la varianza muestral por el VAR.S
    # usado en el excel en vez de VAR.P
    variance = sum_sq_diff / length
    return variance


def read_file(filename):
    """
    Read the input file

    Args:
        filename (string): Name of the file with the numbers list

    Returns:
        numbers (list): List of valid numbers
        count (int): Count of file entries (valid and invalid)
    """
    count = 0
    numbers = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                clean_line = line.strip()
                count = count + 1
                if not clean_line:
                    continue
                try:
                    numbers.append(float(clean_line))
                except ValueError:
                    print(f"Error: Invalid number encountered and skipped: \
                    {clean_line}'")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, 0
    return numbers, count


def print_and_save_data(data_to_print, start_time):
    """
    Print results to output file and console

    Args:
        data_to_print (list): list of tuples with results
        start_time (float): start time of the program
    """
    try:
        with open("StatisticsResults.txt", 'w', encoding='utf-8') as out_file:
            for label, value in data_to_print:
                line = f"{label:<20} | {value:<20}"
                print(line)
                out_file.write(line + "\n")
            elapsed_time = time.time() - start_time
            print(f"Elapsed Time: {elapsed_time:.4f} seconds")
            out_file.write(f"Elapsed Time: {elapsed_time:.4f} seconds")
    except IOError as e:
        print(f"Error writing to file: {e}")


def main():
    """Main execution function."""
    start_time = time.time()

    if len(sys.argv) < 2:
        print("Error format: python computeStatistics.py <fileWithData.txt>")
        return

    numbers, count = read_file(sys.argv[1])

    if not numbers:
        print("Error: No valid numbers found in the file.")
        mean = 0
        median = 0
        mode = 0
        variance = 0
        std_dev = 0
        mode_string = "N/A"
    else:
        # Using length of valid numbers for the statistical calculation
        length = len(numbers)
        mean = calculate_mean(numbers, length)
        median = calculate_median(numbers, length)
        mode = calculate_mode(numbers)
        variance = calculate_variance(numbers, mean, length)
        std_dev = variance ** (1.0/2.0)

        if len(mode) == length:
            mode_string = "N/A"
        else:
            # Printing only the first Mode to match the expected result
            mode_string = str(mode[0])

    data_to_print = [
        ("Statistic", "Value"),
        ("-" * 20, "-" * 20),
        ("Count", count),
        ("Mean", f"{mean:.4f}"),
        ("Median", f"{median:.2f}"),
        ("Mode", mode_string),
        ("Std Deviation", f"{std_dev:.4f}"),
        ("Variance", f"{variance:.4f}"),
        ("-" * 20, "-" * 20),
    ]

    print_and_save_data(data_to_print, start_time)


if __name__ == "__main__":
    main()
