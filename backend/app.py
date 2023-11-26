from datetime import date, datetime, timedelta
import os
import logging
import mysql.connector
from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash

# Client IPDict
IPDict = {}

# https://testdriven.io/blog/csrf-flask/
app = Flask(__name__)
cors = CORS(app)
app.config.update(
    DEBUG=True,
    CORS_HEADERS='Content-Type',
)
config = {
  'user': 'root',
  'password': 'test',
  'host': 'db',
  'database': 'myDb',
  'raise_on_warnings': True
}

def initLogger():
    """Create a logger and log file named with today's day + connectionLog.txt """
    today = date.today()
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    logging.basicConfig(filename=f'Logs/{today.strftime("%d%m%y") + "connectionLog.txt"}',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logging.getLogger('Backend').info("The logger is initialized")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    conn = mysql.connector.connect(**config)
    conn.row_factory = dict_factory
    return conn

def checkpassword(name, password):
    conn = get_db_connection()
    if conn and conn.is_connected():
        cursor = conn.cursor(prepared=True, dictionary=True)
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursorprepared.html
        stmtP = "SELECT * FROM Patients where username = %s"
        cursor.execute(stmtP) # prepare the statement
        cursor.execute(stmtP, (name,)) # execute the prepared statement
        logging.getLogger('Backend').info(stmtP + name)
        user = cursor.fetchall()
        isStaff = False
        role = ""
        if len(user) == 0: # not Patient user
            stmtS = "SELECT * FROM Staff where username = %s"
            cursor.execute(stmtS) # prepare the statement
            cursor.execute(stmtS, (name,)) # execute the prepared statement
            user = cursor.fetchall()
            isStaff = True
    conn.close()

    if user is None:
        json_data = {"isvalid":False,"from client": request.remote_addr,
                        "attempt count": IPDict[request.remote_addr][0],
                        "status": "User not exist in database!"}
        return json_data

    for row in user:
        hashedpw = row['pwHash']
        if isStaff: 
            role = row['role']
            id = row['staff_id']
        else:
            id = row['patient_id']

    if check_password_hash(hashedpw, password):
        # update the format of hash before send to client
        userDict = {}
        userDict["pwHash"] = password
        userDict["isStaff"] = isStaff
        userDict["name"] = name
        userDict["id"] = id
        json_data = {"isvalid":True, "from client": request.remote_addr,
                    "User info": userDict, "role": role}
        return json_data
    else:
        json_data = {"isvalid":False, "from client": request.remote_addr,
                    "attempt count": IPDict[request.remote_addr][0], "status": "password not match"}
        return json_data

def getDBCredByRole(isVaildRequest):
    if isVaildRequest['role'] == 'lab_staff':
        dbUser = 'LS'
        dbPW = 'lab_staff'
    elif isVaildRequest['role'] == 'secretaries':
        dbUser = 'SE'
        dbPW = 'secretaries'
    else:
        dbUser = 'PA'
        dbPW = 'patients'
    return dbUser, dbPW

# This route is for testing use only.
@app.route("/")
def main():
    return "Wellcome to COMP3335 Backend!" 

@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    # check if brute force trying password to login
    if request.remote_addr not in IPDict:
        IPDict[request.remote_addr] = [0, datetime.now()]
    else:
        # reset the count to unblock user after 5 minutes
        if datetime.now() - IPDict[request.remote_addr][1] > timedelta(minutes=5):
            IPDict[request.remote_addr] = [0, datetime.now()]

        if IPDict[request.remote_addr][0] == 5:
            json_data = {"isvalid":False, "from client": request.remote_addr, 
                          "attempt count": IPDict[request.remote_addr][0], 
                          "status": "This IP is blocked 5 minutes since too many\
                                    failed login attempts"}
            return jsonify(json_data), 200
        IPDict[request.remote_addr][0] = IPDict[request.remote_addr][0] + 1

    json_data = request.get_json()
    name = json_data['name']
    password = json_data['pwHash']

    json_data = checkpassword(name, password)
    return jsonify(json_data), 200

@app.route('/api/getResults', methods=['POST'])
@cross_origin()
def getResults():
    json_data = request.get_json()
    name = json_data['name']
    password = json_data['pwHash']

    isVaildRequest = checkpassword(name, password)
    if isVaildRequest['isvalid'] == False:
        return isVaildRequest, 200

    conn = get_db_connection()
    if conn and conn.is_connected():
        dbUser, dbPW = getDBCredByRole(isVaildRequest)
        conn.cmd_change_user(username=dbUser, password=dbPW, database='myDb')
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM Results")
            results = cursor.fetchall()
    conn.close()
    return jsonify(results), 200

@app.route('/api/updateResult', methods=['POST'])
@cross_origin()
def updateResult():
    json_data = request.get_json()
    name = json_data['name']
    password = json_data['pwHash']
    order_id = json_data['order_id']
    report_url = json_data['report_url']
    interpretation = json_data['interpretation']

    isVaildRequest = checkpassword(name, password)
    if isVaildRequest['isvalid'] == False:
        return isVaildRequest, 200

    conn = get_db_connection()
    if conn and conn.is_connected():
        dbUser, dbPW = getDBCredByRole(isVaildRequest)
        conn.cmd_change_user(username=dbUser, password=dbPW, database='myDb')
        with conn.cursor(dictionary=True) as cursor:
            sql = "INSERT INTO Results (order_id, report_url, interpretation, reporting_pathologist) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (order_id, report_url, interpretation, name))
            logging.getLogger('Backend').info(sql, order_id, report_url, interpretation, name)
            conn.commit()
    conn.close()
    return jsonify("updated!"), 200

@app.route('/api/getOrder', methods=['POST'])
@cross_origin()
def getOrder():
    json_data = request.get_json()
    name = json_data['name']
    id = json_data['id']
    password = json_data['pwHash']

    isVaildRequest = checkpassword(name, password)
    if isVaildRequest['isvalid'] == False:
        return isVaildRequest, 200

    conn = get_db_connection()
    if conn and conn.is_connected():
        dbUser, dbPW = getDBCredByRole(isVaildRequest)
        conn.cmd_change_user(username=dbUser, password=dbPW, database='myDb')
        with conn.cursor(dictionary=True) as cursor:
            sql = "SELECT O.order_id, O.order_date, T.name AS test_name, O.ordering_physician, O.status \
                    FROM Orders AS O JOIN Tests_Catalog AS T ON O.test_id = T.test_id \
                    WHERE O.patient_id = %s"
            cursor.execute(sql, (id,))
            logging.getLogger('Backend').info(sql + str(id))
            results = cursor.fetchall()
    conn.close()
    return jsonify(results), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=15000, debug=True, use_reloader=True)
    initLogger()
