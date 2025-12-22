import pandas as pd


def find_values_for_code(file_path, target_code, filter_negative=False, show_all=False):
    """
    Reads a CSV file and returns all 'value' entries for a given 'code' as a pandas Series.
    Optionally filters only negative values.
    Optionally sets display options to show all values without truncation.

    :param file_path: Path to the CSV file
    :param target_code: The code to filter by
    :param filter_negative: If True, return only negative values (default: False)
    :param show_all: If True, set pandas display options to show all rows (default: False)
    :return: Pandas Series of values for the given code (filtered if requested)
    """
    if show_all:
        pd.set_option('display.max_rows', None)
        pd.set_option('display.min_rows', None)

    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Filter the DataFrame for the target code
    filtered_df = df[df['code'] == target_code]

    # Optionally filter for negative values
    if filter_negative:
        filtered_df = filtered_df[filtered_df['value'] < 0]

    # Extract the 'value' column as a Series
    values_series = filtered_df[['value', 'tax_id']]

    return values_series

def get_column(file_path, column_name):
    return pd.read_csv(file_path)[column_name]


if __name__ == "__main__":
    # pd.set_option('display.max_rows', None)  # Показує всі рядки
    # result = find_values_for_code("fin_values.csv", 1495)

    # empty_fields = pd.read_csv('fin_values_test.csv').isnull().sum()
    # print(f'Empty fields\n: {empty_fields}')

    duplicated_fields = pd.read_csv('fin_values.csv').duplicated().sum()
    print(f'Duplicate fields\n: {duplicated_fields}')

    # print(result)
    # result.to_csv('output.csv', index=False)