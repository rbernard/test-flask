from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL
import sys

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'myproject'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # first_name = request.form['fname']
        # last_name = request.form['lname']
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO Users(firstName, lastName) VALUES (%s, %s)", (first_name, last_name))
        # mysql.connection.commit()
        # cur.close()
        return display_page()

    return display_page()


@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Users WHERE id = %s", [user_id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))


def display_page():
    first_letters = read_first_letters()
    first_letter_selected = request.args.get('firstLetterSelected')
    second_letters = read_second_letters(first_letter_selected)
    second_letter_selected = request.args.get('secondLetterSelected')
    words = read_words(first_letter_selected, second_letter_selected)

    print(request.args)
    return render_template('index.html', first_letters=first_letters, second_letters=second_letters, words=words)


def read_first_letters():
    cursor = mysql.connection.cursor()
    cursor.execute("select DISTINCT LEFT(Word, 1) FROM WORDS")
    return cursor.fetchall()


def read_second_letters(first_letter):
    if first_letter is None:
        return []
    cursor = mysql.connection.cursor()
    cursor.execute("select DISTINCT LEFT(Word, 2) FROM WORDS WHERE LEFT(Word, 1) = %s", first_letter)
    return cursor.fetchall()


def read_words(first_letter, second_letter):
    print(first_letter)
    print(second_letter)
    if first_letter is None:
        return []

    if second_letter is None:
        cursor = mysql.connection.cursor()
        cursor.execute("select Word FROM WORDS WHERE LEFT(Word, 1) = %s", [first_letter])
        return cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("select Word FROM WORDS WHERE LEFT(Word, 2) = %s", [second_letter])
    return cursor.fetchall()


if __name__ == '__main__':
    app.run()
