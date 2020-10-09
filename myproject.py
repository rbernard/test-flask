from flask import Flask, redirect, url_for, render_template, request, redirect
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


@app.route('/definitions', methods=['GET'])
def definitions():
    return render_template('definition.html', definitions=read_definitions(request.args.get('word')))


def display_page():
    first_letter_selected = request.args.get('firstLetterSelected')
    second_letter_selected = request.args.get('secondLetterSelected')
    word_selected = request.args.get('wordSelected')

    first_letters = read_first_letters()
    second_letters = read_second_letters(first_letter_selected)
    should_redirect = False
    if second_letter_selected is not None and second_letter_selected not in map(lambda x: x[0], second_letters):
        second_letter_selected = None
        word_selected = None
        should_redirect = True
    words = read_words(first_letter_selected, second_letter_selected)
    if word_selected is not None and word_selected not in map(lambda x: x[0], words):
        word_selected = None
        should_redirect = True

    if should_redirect:
        return redirect(
            url_for('index', firstLetterSelected=first_letter_selected, secondLetterSelected=second_letter_selected,
                    wordSelected=word_selected))

    return render_template('index.html', first_letters=first_letters, second_letters=second_letters, words=words)


def read_definitions(word):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT Type, Definition FROM Words WHERE Word=%s", [word])
    return cursor.fetchall()


def read_first_letters():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT LEFT(Word, 1) FROM Words ORDER BY LEFT(Word, 1)")
    return cursor.fetchall()


def read_second_letters(first_letter):
    if first_letter is None:
        return []
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT LEFT(Word, 2) FROM Words WHERE LEFT(Word, 1) = %s ORDER BY LEFT(Word, 2)",
                   first_letter)
    return cursor.fetchall()


def read_words(first_letter, second_letter):
    if first_letter is None:
        return []

    if second_letter is None:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DISTINCT Word FROM Words WHERE LEFT(Word, 1) = %s ORDER BY Word",
                       [first_letter])
        return cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT Word FROM Words WHERE LEFT(Word, 2) = %s ORDER BY Word", [second_letter])
    return cursor.fetchall()


if __name__ == '__main__':
    app.run()
