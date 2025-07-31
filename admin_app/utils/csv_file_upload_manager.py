import csv


def parse_questions_from_csv(file: any):
    if not file.name.endswith('.csv') and not file.name.endswith('.tsv'):
        return None, []
    questions_file = file
    decoded_file = questions_file.read().decode('utf-8').splitlines()
    delimiter = ',' if questions_file.name.endswith('.csv') else '\t'
    reader = csv.DictReader(decoded_file, delimiter=delimiter)
    table_heads = next(csv.reader(decoded_file, delimiter=delimiter), None)
    rows = list(reader)
    return table_heads, rows
