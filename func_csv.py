import csv
def to_table():
    with open("questions.csv", mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        table_questions = [{key : value for key, value in element.items()} for element in reader]
    return table_questions
