import os
import pyodbc
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Database
conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:scoresheet.database.windows.net,1433;Database=score_sheet_db;Uid=scoresheetAdmin;Pwd=ss@27365410;Encrypt=yes;TrustServerCertificate=no;")
cursor = conn.cursor()

@app.route('/', methods=['GET'])
def getIP():

    if(request.method == 'GET'):

        try:
            query = 'SELECT D.DeviceId, D.Address FROM Devices D'
            cursor.execute(query)
            res = cursor.fetchone()
            data = {
                'DeviceId': res.DeviceId,
                'Address': res.Address,
            }

            return jsonify(data), 200

        except  Exception as err:
            print(err)
            return jsonify(), 500


@app.route('/updateAddress', methods=['POST'])
def updateAddress():

    new_address = request.args.get('Address')
    device_id = 1
    if(request.method == 'POST'):

        try:
            query = '''
                UPDATE Devices
                SET Address=?
                WHERE DeviceId=?
            '''

            cursor.execute(query,(new_address,device_id))
            cursor.commit()

            return jsonify(True), 200
        
        except Exception as err:
            print(err)
            return jsonify(), 500

app.run()
# app.run(debug=True, host="0.0.0.0",port=5000)