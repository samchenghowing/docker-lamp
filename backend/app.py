from datetime import date, datetime, timedelta
import time
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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    conn = mysql.connector.connect(**config)
    conn.row_factory = dict_factory
    return conn

def is_inappropriate_access(query_string):
    query_string = query_string.lower()
    if "select" in query_string:
        return True
    elif "update" in query_string:
        return True
    if "delete" in query_string:
        return True
    if "insert" in query_string:
        return True
    if "drop" in query_string:
        return True
    if "create" in query_string:
        return True
    return False

def vaildateSQL(query_string, ipaddr):
    if is_inappropriate_access(query_string):
        writeErrorLog(query_string, ipaddr)

def writeErrorLog(query_string, ipaddr):
    ipStr = str(ipaddr)
    conn = get_db_connection()
    if conn and conn.is_connected():
        conn.cmd_change_user(username='root', password='test', database='myDb')
        with conn.cursor(dictionary=True) as cursor:
            currentT = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            sql = "INSERT INTO SuspiciousLog (log_date, log_info, send_from) VALUES (%s, %s, %s)"
            cursor.execute(sql, (currentT, query_string, ipStr))
            conn.commit()
    conn.close()

def checkpassword(name, password):
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor(prepared=True, dictionary=True)
            # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursorprepared.html
            stmtP = "SELECT * FROM Patients where username = %s"
            if vaildateSQL(name, request.remote_addr):
                json_data = {"isvalid":False, "from client": request.remote_addr,
                            "attempt count": IPDict[request.remote_addr][0], "status": "possiable sql injection attempt"}
                return json_data

            cursor.execute(stmtP) # prepare the statement
            cursor.execute(stmtP, (name,)) # execute the prepared statement
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
    except mysql.connector.Error as err:
        writeErrorLog("MySQL error: {}".format(err), request.remote_addr)
        return jsonify("Error!"), 200

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

@app.errorhandler(500)
def code_500(error):
    return (error), 500

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

# the signup function is neighter used nor exposed to the
# REST API, only for illustrating signup process
# @app.route('/api/signup', methods=['POST'])
# @cross_origin()
def signup():
    json_data = request.get_json()
    name = json_data['name']
    password = json_data['pwHash']

    # check if user exist in database
    conn = get_db_connection()
    sql_select_query = """select * from users where name = %s"""
    res = conn.execute(sql_select_query, (name,)).fetchone()
    if res is not None:
        json_data = {"signup":False, "status": "User alreafy exist in database!"}
        return jsonify(json_data), 200

    # TO-DO: email verification

    hash = generate_password_hash(password)
    conn.execute("INSERT INTO users (name, pwHash) VALUES (%s, %s, %s)",
                (name, hash, 0)
                )
    
    conn.commit()
    conn.close()

    json_data = {"signup":True}
    return jsonify(json_data), 200

@app.route('/api/getResults', methods=['POST'])
@cross_origin()
def getResults():
    json_data = request.get_json()
    name = json_data['name']
    password = json_data['pwHash']
    id = json_data['id']

    isVaildRequest = checkpassword(name, password)
    if isVaildRequest['isvalid'] == False:
        return isVaildRequest, 200

    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            dbUser, dbPW = getDBCredByRole(isVaildRequest)
            conn.cmd_change_user(username=dbUser, password=dbPW, database='myDb')
            with conn.cursor(dictionary=True) as cursor:
                if dbUser == 'PA':
                    sql = "SELECT r.result_id, r.order_id, r.report_url, r.interpretation, r.reporting_pathologist\
                            FROM Results r JOIN Orders o ON r.order_id = o.order_id\
                            WHERE o.patient_id = %s; "
                    if vaildateSQL(str(id), request.remote_addr):
                        return jsonify("possiable injection detected"), 200
                    cursor.execute(sql, (id,))
                elif dbUser == 'LS':
                    cursor.execute("SELECT * FROM Results")
                else:
                    cursor.execute("SELECT result_id, order_id, report_url FROM Results")
                results = cursor.fetchall()
        conn.close()
    except mysql.connector.Error as err:
        writeErrorLog("MySQL error: {}".format(err), request.remote_addr)
        return jsonify("Error!"), 200
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

    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            dbUser, dbPW = getDBCredByRole(isVaildRequest)
            conn.cmd_change_user(username=dbUser, password=dbPW, database='myDb')
            with conn.cursor(dictionary=True) as cursor:
                sql = "INSERT INTO Results (order_id, report_url, interpretation, reporting_pathologist) VALUES (%s, %s, %s, %s)"
                if vaildateSQL(str(order_id)+ str(report_url) + str(interpretation)+ str(name), request.remote_addr):
                    return jsonify("prossible injection!"), 200
                cursor.execute(sql, (order_id, report_url, interpretation, name))
                conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        writeErrorLog("MySQL error: {}".format(err), request.remote_addr)
        return jsonify("Error!"), 200
    
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

    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            dbUser, dbPW = getDBCredByRole(isVaildRequest)
            conn.cmd_change_user(username=dbUser, password=dbPW, database='myDb')
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT O.order_id, O.order_date, T.name AS test_name, O.ordering_physician, O.status \
                        FROM Orders AS O JOIN Tests_Catalog AS T ON O.test_id = T.test_id \
                        WHERE O.patient_id = %s"
                if vaildateSQL(str(id), request.remote_addr):
                    jsonify("possible injection"), 200
                cursor.execute(sql, (id,))
                results = cursor.fetchall()
        conn.close()
    except mysql.connector.Error as err:
        writeErrorLog("MySQL error: {}".format(err), request.remote_addr)
        return jsonify("Error!"), 200
    
    return jsonify(results), 200

@app.route('/api/getBills', methods=['POST'])
@cross_origin()
def getBills():
    json_data = request.get_json()
    name = json_data['name']
    id = json_data['id']
    password = json_data['pwHash']

    isVaildRequest = checkpassword(name, password)
    if isVaildRequest['isvalid'] == False:
        return isVaildRequest, 200

    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            dbUser, dbPW = getDBCredByRole(isVaildRequest)
            conn.cmd_change_user(username=dbUser, password=dbPW, database='myDb')
            with conn.cursor(dictionary=True) as cursor:
                if dbUser == 'PA':
                    sql = "SELECT b.bill_id, o.order_id, b.billed_amount, b.payment_status, b.insurance_claim_status\
                            FROM Billing b INNER JOIN Orders o ON b.order_id = o.order_id\
                            WHERE o.patient_id = %s"
                    if vaildateSQL(str(id), request.remote_addr):
                        jsonify("possible injection"), 200
                    cursor.execute(sql, (id,))
                else:
                    cursor.execute("SELECT * FROM Billing")
                results = cursor.fetchall()
        conn.close()
    except mysql.connector.Error as err:
        writeErrorLog("MySQL error: {}".format(err), request.remote_addr)
        return jsonify("Error!"), 200
    return jsonify(results), 200

@app.route('/api/updateBills', methods=['POST'])
@cross_origin()
def updateBills():
    json_data = request.get_json()
    name = json_data['name']
    password = json_data['pwHash']
    bill_id = json_data['bill_id']
    billed_amount = json_data['billed_amount']
    payment_status = json_data['payment_status']
    insurance_claim_status = json_data['insurance_claim_status']

    isVaildRequest = checkpassword(name, password)
    if isVaildRequest['isvalid'] == False:
        return isVaildRequest, 200

    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            dbUser, dbPW = getDBCredByRole(isVaildRequest)
            conn.cmd_change_user(username=dbUser, password=dbPW, database='myDb')
            with conn.cursor(dictionary=True) as cursor:
                sql = "UPDATE Billing SET billed_amount = %s,\
                        payment_status = %s,\
                        insurance_claim_status = %s\
                        WHERE bill_id = %s;"
                if vaildateSQL(str(bill_id)+ str(billed_amount) + str(payment_status)+ str(insurance_claim_status), request.remote_addr):
                    return jsonify("prossible injection!"), 200
                cursor.execute(sql, (billed_amount, payment_status, insurance_claim_status, bill_id))
                conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        writeErrorLog("MySQL error: {}".format(err), request.remote_addr)
        return jsonify("Error!"), 200
    return jsonify("updated!"), 200

@app.route('/api/getAppointments', methods=['POST'])
@cross_origin()
def getAppointments():
    json_data = request.get_json()
    name = json_data['name']
    password = json_data['pwHash']

    isVaildRequest = checkpassword(name, password)
    if isVaildRequest['isvalid'] == False:
        return isVaildRequest, 200

    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            dbUser, dbPW = getDBCredByRole(isVaildRequest)
            conn.cmd_change_user(username=dbUser, password=dbPW, database='myDb')
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT * from Appointments"
                cursor.execute(sql)
                results = cursor.fetchall()
        conn.close()
    except mysql.connector.Error as err:
        writeErrorLog("MySQL error: {}".format(err), request.remote_addr)
        return jsonify("Error!"), 200
    return jsonify(results), 200

@app.route('/api/updateAppointments', methods=['POST'])
@cross_origin()
def updateAppointments():
    json_data = request.get_json()
    name = json_data['name']
    password = json_data['pwHash']
    patient_id = json_data['patient_id']
    appointment_date = json_data['appointment_date']

    isVaildRequest = checkpassword(name, password)
    if isVaildRequest['isvalid'] == False:
        return isVaildRequest, 200
    
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            dbUser, dbPW = getDBCredByRole(isVaildRequest)
            conn.cmd_change_user(username=dbUser, password=dbPW, database='myDb')
            with conn.cursor(dictionary=True) as cursor:
                sql = "INSERT INTO Appointments (patient_id, appointment_date) VALUES (%s, %s)"
                if vaildateSQL(str(patient_id)+ str(appointment_date), request.remote_addr):
                    return jsonify("prossible injection!"), 200
                date_object = datetime.strptime(appointment_date, "%Y-%m-%d").date()
                datetime_object = datetime.combine(date_object, datetime.min.time())
                date = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(sql, (patient_id, date))
                conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        writeErrorLog("MySQL error: {}".format(err), request.remote_addr)
        return jsonify("Error!"), 200
    return jsonify("updated!"), 200

@app.route('/api/getLog', methods=['POST'])
@cross_origin()
def getLog():
    json_data = request.get_json()
    name = json_data['name']
    password = json_data['pwHash']

    isVaildRequest = checkpassword(name, password)
    if isVaildRequest['isvalid'] == False:
        return isVaildRequest, 200

    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT * from SuspiciousLog"
                cursor.execute(sql)
                results = cursor.fetchall()
        conn.close()
    except mysql.connector.Error as err:
        writeErrorLog("MySQL error: {}".format(err), request.remote_addr)
        return jsonify("Error!"), 200
    return jsonify(results), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=15000, debug=False, use_reloader=True)
