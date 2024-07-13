from flask import Flask, render_template, request, jsonify
import pymongo
from pymongo import MongoClient
from encryption import encrypt, decrypt  
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transfer', methods=['POST'])
def transfer_data():
    try:
        mysql_host = request.form['mysql_host']
        mysql_user = request.form['mysql_user']
        mysql_password = request.form['mysql_password']
        mysql_db = request.form['mysql_db']
        mysql_table = request.form['mysql_table']

        mongo_uri = request.form['mongo_uri']
        mongo_db = request.form['mongo_db']
        mongo_collection_name = request.form['mongo_collection']

        MYSQL_CONFIG = {
            'host': mysql_host,
            'user': mysql_user,
            'password': mysql_password,
            'database': mysql_db,
        }

        mongo_client = MongoClient(mongo_uri)
        mongo_db = mongo_client[mongo_db]
        mongo_collection = mongo_db[mongo_collection_name]

        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)

        query = f"SELECT * FROM {mysql_table}"
        mysql_cursor.execute(query)
        rows = mysql_cursor.fetchall()

        shift_value = 3

        for row in rows:
            encrypted_row = {key: encrypt(str(value), shift_value) for key, value in row.items()}
            mongo_collection.insert_one(encrypted_row)

        mysql_conn.close()
        mongo_client.close()

        return render_template('transfer_success.html', count=len(rows))

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return render_template('transfer_error.html', error_message=error_message)

@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    try:
        mongo_uri = request.form['mongo_uri']
        mongo_db_name = request.form['mongo_db']
        mongo_collection_name = request.form['mongo_collection']

        mongo_client = MongoClient(mongo_uri)
        mongo_db = mongo_client[mongo_db_name]
        mongo_collection = mongo_db[mongo_collection_name]

        shift_value = 3

        for document in mongo_collection.find():
            decrypted_document = {key: decrypt(str(value), shift_value) if key != '_id' else value for key, value in document.items()}
            mongo_collection.update_one({'_id': document['_id']}, {'$set': decrypted_document})

        mongo_client.close()

        return render_template('decrypt_success.html')

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return render_template('decrypt_error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
