"""
computeSales.py
@author: Carlos Antonio Heinze Mortera A01700179
Program that takes the JSON of a product catalogue and sales
and sales record, and calculates the total sales to show the
user.
"""
import json
import sys
import time


def process_json(file_path):
    """
    Loads a JSON file and returns the data.

    Args:
        file_path (str): File path to the JSON to load.

    Returns:
        (dict or list): python onject representing the JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error {e} in file {file_path}")
        return None


def calculate_total_sales(catalogue, sales):
    """
    Computes total sales and handles missing items.

    Args:
        file_path (str): File path to the JSON to load.

    Returns:
        total_cost (float): total cost of all the sales in the JSON.
        errors (int): total errors found in the JSON.
    """
    total_cost = 0.0
    errors = 0
    catalogue_dict = {}
    # Create a dictionary with prices for each items for lookup
    for item in catalogue:
        catalogue_dict[item["title"]] = item["price"]

    # Use .get to access the dictionary to have a None or 0 in case the
    # key does not exist in the given dictionary
    for sale in sales:
        product = sale.get("Product")
        quantity = sale.get("Quantity", 0)
        price = catalogue_dict.get(product)

        if (price is not None) and (quantity != 0):
            total_cost += price * quantity
        else:
            sale_id = sale.get("SALE_ID")
            print(f"Error in SALE {sale_id} with product '{product}'")
            errors += 1

    return total_cost, errors


def main():
    """Main execution function."""
    start_time = time.time()

    if len(sys.argv) != 3:
        print("Error use command: python computeSales.py "
              "priceCatalogue.json salesRecord.json")
        return

    catalogue_file = sys.argv[1]
    sales_file = sys.argv[2]

    # Load data
    catalogue_data = process_json(catalogue_file)
    sales_data = process_json(sales_file)

    if catalogue_data is None or sales_data is None:
        return

    # Process data
    total, errors = calculate_total_sales(catalogue_data, sales_data)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Prepare output
    output = []
    output.append("-" * 30)
    output.append("SALES EXECUTION RESULTS")
    output.append("-" * 30)
    output.append(f"Total Sales Cost: ${total:,.2f}")
    output.append(f"Execution Time: {elapsed_time:.4f} seconds")
    output.append("-" * 30)
    if errors:
        output.append(f"Errors encountered: {errors}")

    final_result = "\n".join(output)

    # Display and Save
    print(final_result)
    with open("SalesResults.txt", "w", encoding="utf-8") as f:
        f.write(final_result)


if __name__ == "__main__":
    main()
