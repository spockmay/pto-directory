import csv


def load_csv_to_dict_list(filepath):
    """
    Loads data from a CSV file and returns it as a list of dictionaries.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries, where each dictionary is a row.
              Returns an empty list if the file is not found or is empty (besides header).
    """
    data_list = []
    try:
        with open(filepath, mode="r", newline="", encoding="utf-8") as csvfile:
            # csv.DictReader uses the first row as keys (fieldnames)
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Each row is an OrderedDict by default, convert it to a standard dict
                data_list.append(dict(row))
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return []

    return data_list
