from flask import Flask, request, jsonify, make_response
import mysql.connector

app = Flask(__name__)
app.config["DEBUG"] = True

mydb = mysql.connector.connect(
  host="OlafArtAnanda.mysql.pythonanywhere-services.com",
  user="OlafArtAnanda",
  password="4getitnow",
  database="OlafArtAnanda$manifestation"
)
#mycursor = mydb.cursor()
#mycursor.execute("DROP TABLE user")
#mycursor.execute("CREATE TABLE newsletter (id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255), name VARCHAR(255), listname VARCHAR(255))")

@app.route('/', methods=['GET'])
def home():
    return 'Hello from the Newsletter app'

@app.route('/newsletter/all', methods=['GET'])
def api_all():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM newsletter")
    myresult = mycursor.fetchall()
    response = jsonify(myresult)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/newsletter/<int:id>', methods=['GET'])
def api_id(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM newsletter where id = " + str(id))
    myresult = mycursor.fetchall()
    return jsonify(myresult)

@app.route('/newsletter', methods=['POST','OPTIONS'])
def api_add():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
    else:
        json = request.json
        email = json['email']
        name = "myname"#json['name']
        listname = "mylist"#json['listname']

        if name and email:
            sql = "INSERT INTO newsletter (name, email, listname) VALUES (%s, %s, %s)"
            val = (name, email, listname)
            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()
            response = jsonify('User added to newsletter successfully!')
            response.status_code = 200
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add('Access-Control-Allow-Headers', "*")
            response.headers.add('Access-Control-Allow-Methods', "*")
            return response
        else:
            return not_found()

@app.route('/newsletter', methods=['PUT'])
def api_update():
    json = request.json
    id = json['id']
    email = json['email']
    name = json['name']
    listname = json['listname']

    if id and name and email and listname:
        sql = "UPDATE newsletter SET name=%s, email=%s, listname=%s WHERE id=%s"
        val = (name, email, listname, id)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        respone = jsonify('User in newsletter has been updated successfully!')
        respone.status_code = 200
        return respone
    else:
        return not_found()

@app.route('/newsletter/<int:id>', methods=['DELETE'])
def api_delete(id):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM newsletter WHERE id =%s", (id,))
    mydb.commit()
    respone = jsonify('User deleted from newsletter successfully!')
    respone.status_code = 200
    return respone

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
