#importing necessary libs
from flask import Flask, render_template, request, jsonify
import pymongo
from pymongo import MongoClient
# Import your encryption functions from encryption.py
from encryption import encrypt, decrypt  
import pymysql

#Initializing Flask App
app = Flask(__name__)

# Render the form to enter MySQL and MongoDB details
@app.route('/')
def index():
    return render_template('index.html')

# App Route to handle form submission to transfer data
@app.route('/transfer', methods=['POST'])
def transfer_data():
    try:
        # Retrieve MySQL and MongoDB configuration details from form
        mysql_host = request.form['mysql_host']
        mysql_user = request.form['mysql_user']
        mysql_password = request.form['mysql_password']
        mysql_db = request.form['mysql_db']

        mongo_uri = request.form['mongo_uri']
        mongo_db = request.form['mongo_db']
        mongo_collection_name = request.form['mongo_collection']

        # MySQL Configuration
        MYSQL_CONFIG = {
            'host': mysql_host,
            'user': mysql_user,
            'password': mysql_password,
            'database': mysql_db,
        }

        # MongoDB Configuration
        mongo_client = MongoClient(mongo_uri)
        mongo_db = mongo_client[mongo_db]
        mongo_collection = mongo_db[mongo_collection_name]

        # Connect to MySQL
        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)

        # Fetch data from MySQL
        mysql_cursor.execute("SELECT * FROM url_hits")
        rows = mysql_cursor.fetchall()

        # Encryption shift value
        shift_value = 3

        # Encrypt and transfer data to MongoDB
        for row in rows:
            encrypted_row = {key: encrypt(str(value), shift_value) for key, value in row.items()}
            mongo_collection.insert_one(encrypted_row)

        # Close connections
        mysql_conn.close()
        mongo_client.close()

        # Return success message with count of records transferred
        return render_template('transfer_success.html', count=len(rows))

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return render_template('transfer_error.html', error_message=error_message)

# App route to handle form submission to decrypt data
@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    try:
        # Retrieve MongoDB configuration details from form
        mongo_uri = request.form['mongo_uri']
        mongo_db_name = request.form['mongo_db']
        mongo_collection_name = request.form['mongo_collection']

        # MongoDB Configuration
        mongo_client = MongoClient(mongo_uri)
        mongo_db = mongo_client[mongo_db_name]
        mongo_collection = mongo_db[mongo_collection_name]

        # Encryption shift value
        shift_value = 3

        # Decrypt data in MongoDB collection
        for document in mongo_collection.find():
            decrypted_document = {key: decrypt(str(value), shift_value) if key != '_id' else value for key, value in document.items()}
            mongo_collection.update_one({'_id': document['_id']}, {'$set': decrypted_document})

        # Close connection
        mongo_client.close()

        # Return success message
        return render_template('decrypt_success.html')

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return render_template('decrypt_error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
