from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'myproject'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return display_page()


def display_page():
    first_letters = read_first_letters()
    first_letter_selected = request.args.get('firstLetterSelected')
    second_letters = read_second_letters(first_letter_selected)
    second_letter_selected = request.args.get('secondLetterSelected')
    words = read_words(first_letter_selected, second_letter_selected)
    return render_template('index.html', first_letters=first_letters, second_letters=second_letters, words=words)


def read_first_letters():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT LEFT(Word, 1) FROM Words")
    return cursor.fetchall()


def read_second_letters(first_letter):
    if first_letter is None:
        return []
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT LEFT(Word, 2) FROM Words WHERE LEFT(Word, 1) = %s", first_letter)
    return cursor.fetchall()


def read_words(first_letter, second_letter):
    if first_letter is None:
        return []

    if second_letter is None:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Word FROM Words WHERE LEFT(Word, 1) = %s", [first_letter])
        return cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT Word FROM Words WHERE LEFT(Word, 2) = %s", [second_letter])
    return cursor.fetchall()


if __name__ == '__main__':
    app.run()
