import sys
import mysql.connector
import csv

from pathlib import Path

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="myproject", auth_plugin='mysql_native_password'
)


def clear():
    my_cursor = mydb.cursor()
    my_cursor.execute("TRUNCATE TABLE Words")


def insert(word, t, definition):
    my_cursor = mydb.cursor()
    my_cursor.execute("INSERT INTO Words (Word, Type, Definition) VALUES (%s, %s, %s)", [word, t, definition])
    mydb.commit()


def main(directory):
    clear()
    files = list(Path(directory).glob('*'))
    for entry in files:
        print(f"importing {entry.name}...")
        with open(entry, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"', skipinitialspace=True)
            for row in reader:
                if len(row) == 3:
                    [word, t, definition] = row
                    insert(word, t, definition)
                else:
                    print(f"Error importing row: {row}")


if __name__ == "__main__":
    # unzip https://github.com/manassharma07/English-Dictionary-CSV/archive/master.zip in dictionary/
    main(sys.argv[1] if len(sys.argv) >= 2 else 'dictionary')
