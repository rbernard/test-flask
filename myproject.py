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
    if request.method == "POST":
        details = request.form
        first_name = details['fname']
        last_name = details['lname']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users(firstName, lastName) VALUES (%s, %s)", (first_name, last_name))
        mysql.connection.commit()
        cur.close()
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
    cursor = mysql.connection.cursor()
    cursor.execute("select firstName, lastName, id from Users")
    data = cursor.fetchall()
    return render_template('index.html', value=data)


if __name__ == '__main__':
    app.run()
