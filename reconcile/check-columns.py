import csv


def find_column_values(file_path):
    column_a_values = set()
    column_b_values = set()

    # Open the CSV file and read its contents
    with open(file_path, mode='r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')

        # Iterate over each row and collect values from columns A and B
        for row in csvreader:
            column_a_values.add(row[0])
            column_b_values.add(row[1])

    return (column_a_values, column_b_values)


file_path = 'reconcile.csv'
(A, B) = find_column_values(file_path)
unique_values = sorted(A - B)
print("Column A values: ", sorted(A))
print("")
print("Column B values: ", sorted(B))
print("")
print("Values in both A and B: ", sorted(set.intersection(A, B)))
print("")
print("Values in column A not in column B: ", unique_values)
