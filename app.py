import json
import yaml
import mysql.connector

from flask import Flask, render_template, request

app = Flask(__name__)
db = mysql.connector.connect(
    host='your_host',
    user='your_user',
    password='your_password',
    database='your_database'
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/populate', methods=['POST'])
def populate_table():
    try:
        data = request.get_json()  # Assumes JSON data is sent in the request body
        if not data:
            return "No data found.", 400

        cursor = db.cursor()
        for row in data:
            for field, value in row.items():
                sql = "INSERT INTO your_table (field, value) VALUES (%s, %s)"
                cursor.execute(sql, (field, value))
        db.commit()
        cursor.close()
        return "Data added to the table successfully."

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
