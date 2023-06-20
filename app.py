import json
import yaml
import mysql.connector

from flask import Flask, render_template, request, redirect, url_for, flash
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, DB_PORT



app = Flask(__name__)
db = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/populate', methods=['GET', 'POST'])
def populate_table():
    if request.method == 'POST':
        table_name = request.form.get('table')  # Get the specified table name
        if not table_name:
            return "Table name is required.", 400

        # flash('Table name received')
        return redirect(url_for('populate_form', table=table_name))  # Redirect to the populate form with the table name as a parameter

    return render_template('index.html')


@app.route('/api/populate/<table>', methods=['GET', 'POST'])
def populate_form(table):
    try:
        if request.method == 'POST':
            columns = request.form.getlist('column')
            values = request.form.getlist('value')

            if not columns or not values:
                return "Columns and values are required.", 400

            cursor = db.cursor()

            placeholders = ', '.join(['%s'] * len(columns))
            sql = "INSERT INTO {} ({}) VALUES ({})".format(table, ', '.join(columns), placeholders)
            cursor.execute(sql, values)

            db.commit()
            cursor.close()
            return "Data added to the table successfully."
        else:
            cursor = db.cursor()

            cursor.execute("DESCRIBE {}".format(table))
            columns = [column[0] for column in cursor.fetchall()]

            cursor.close()
            return render_template('populate.html', table=table, columns=columns)

    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8087)
