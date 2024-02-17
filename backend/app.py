from flask import Flask, jsonify, request
import mysql.connector
import json
import requests

app = Flask(__name__)


@app.route('/api/addUser', methods=['PUT', 'OPTIONS'])
def addUser():
    connection = mysql.connector.connect(
        user='hfnu7wra6kcq609ocsig',
        password='pscale_pw_Vz38uSiRRv1n02HhukMZSMTF1c2QZjHQlphsoc7ZmhK',
        host='aws.connect.psdb.cloud',
        database='subleasingdatabase',
    )

    cursor = connection.cursor()

    rawData = request.json
    firstName = rawData['firstName']
    lastName = rawData['lastName']
    userEmail = rawData['email']
    userPhone = rawData['phoneNumber']

    insert_query = "INSERT INTO users (firstName, lastName, email, phoneNumber) VALUES (%s, %s, %s, %s)"
    data = (firstName, lastName, userEmail, userPhone)

    try:
        # Try to execute the insert query
        cursor.execute(insert_query, data)
        connection.commit()

        response_data = {
            'SUCCESS': 'TRUE',
            'User Added': userEmail
        }
        status_code = 200

    except mysql.connector.IntegrityError as e:
        # Get the error message dynamically
        error_message = str(e)
        response_data = {
            'SUCCESS': 'FALSE',
            'ERROR': error_message
        }
        status_code = 400

    finally:
        cursor.close()
        connection.close()

    json_response = jsonify(response_data)
    json_response.headers.add('Access-Control-Allow-Origin', '*')

    return json_response, status_code


# add listing
@app.route('/api/addListing', methods=['PUT', 'OPTIONS'])
def addListing():
    connection = mysql.connector.connect(
        user='hfnu7wra6kcq609ocsig',
        password='pscale_pw_Vz38uSiRRv1n02HhukMZSMTF1c2QZjHQlphsoc7ZmhK',
        host='aws.connect.psdb.cloud',
        database='subleasingdatabase',
    )

    cursor = connection.cursor()

    rawData = request.json
    pPropertyName = rawData['propertyName']
    pBed = rawData['bed']
    pBath = rawData['bath']
    pRent = rawData['rent']
    pTerm = rawData['term']
    pAddress = rawData['address']
    pGenderPref = rawData['genderPreference']
    userID = rawData['userId']


    insert_query = "INSERT INTO properties (propertyName, bed, bath, rent, term, address, userID, genderPreference)"
    data = (pPropertyName, pBed, pBath, pRent, pTerm, pAddress, pGenderPref, userID)

    try:
        # Try to execute the insert query
        cursor.execute(insert_query, data)
        connection.commit()

        response_data = {
            'SUCCESS': 'TRUE',
            'Listing Added': propertyName
        }
        
        status_code = 200

    except mysql.connector.IntegrityError as e:
        # Get the error message dynamically
        error_message = str(e)
        response_data = {
            'SUCCESS': 'FALSE',
            'ERROR': error_message
        }
        status_code = 400

    finally:
        cursor.close()
        connection.close()

    json_response = jsonify(response_data)
    json_response.headers.add('Access-Control-Allow-Origin', '*')

    return json_response, status_code


@app.route('/api/getListings', methods=['POST'])
def getListings():
    try:
        connection = mysql.connector.connect(
            user='hfnu7wra6kcq609ocsig',
            password='pscale_pw_Vz38uSiRRv1n02HhukMZSMTF1c2QZjHQlphsoc7ZmhK',
            host='aws.connect.psdb.cloud',
            database='subleasingdatabase',
        )

        cursor = connection.cursor()

        rawData = request.json
        start_index = rawData['start']
        end_index = rawData['end']

        select_query = "SELECT * FROM properties LIMIT %s OFFSET %s"
        data = (end_index - start_index, start_index)

        cursor.execute(select_query, data)
        rows = cursor.fetchall()

        # Convert rows to list of dictionaries
        properties_list = []
        for row in rows:
            property_dict = {
                'propertyID': row[0],
                'propertyName': row[1],
                'bed': row[2],
                'bath': row[3],
                'rent': row[4],
                'term': row[5],
                'address': row[6],
                'email': row[7],
                # Add more fields as needed
            }
            properties_list.append(property_dict)

        response_data = {
            'SUCCESS': 'TRUE',
            'listings': properties_list
        }
        status_code = 200

    except mysql.connector.Error as e:
        response_data = {
            'SUCCESS': 'FALSE',
            'ERROR': str(e)
        }
        status_code = 400

    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

    json_response = jsonify(response_data)
    json_response.headers.add('Access-Control-Allow-Origin', '*')

    return json_response, status_code


# #post (update) listing
# @app.route('/api/updateListing', methods = ['POST'])
# def updateListing() :
#     return testResponse


# #get listing
# @app.route('api/getListing', methods = ['GET'])
# def getListing() :
#     return testResponse


# #delete listing
# @app.route('api/deleteListing', methods = ['DELETE'])
# def deleteListing() :
#     return testResponse

if __name__ == '__main__':
    app.run()
