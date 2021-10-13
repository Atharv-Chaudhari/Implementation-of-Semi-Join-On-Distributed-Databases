from flask import Flask, request, url_for, redirect, render_template
from flask_mysqldb import MySQL
import mysql.connector
import socket            
import json

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="manager"
)
mycursor=mydb.cursor()
data=""
name=""

@app.route('/', methods=['POST', 'GET'])
def site2():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="manager"
    )
    mycursor=mydb.cursor()
    tables_names = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='manager'"
    mycursor.execute(tables_names)
    tables = mycursor.fetchall()
    myresult = []
    columns = []
    for i in tables:
        names = "SELECT * FROM "+i[0]
        mycursor.execute(names)
        myresult.append(mycursor.fetchall())
        names = "SELECT Column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= '" + \
            i[0]+"' ORDER BY ORDINAL_POSITION"
        mycursor.execute(names)
        columns.append(mycursor.fetchall())
    s = socket.socket()        
    try:
        s.connect(('127.0.0.1', 12345))
        p=str(s.recv(1024).decode())
        temp=str(s.recv(1024).decode())
        s.close() 
        global data
        global name
        data=temp
        name=p
        temp=temp.split(',')[:-1]
        return render_template('site2.html', table=[], column=[], data=[], n=0,t=temp,po=p)
    except:
        return render_template('site2.html', table=tables, column=columns, data=myresult, n=len(tables),t="",po="")
    #return render_template("server.html")

@app.route('/site2_work', methods=['POST', 'GET'])
def site2_work():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="manager"
    )
    mycursor=mydb.cursor()
    s = socket.socket()
    print ("Socket successfully created")
    s.bind(('', 12345))
    print ("socket binded to %s" %(12345))
    s.listen(5)    
    print ("socket is listening")  
    while True:
        c, addr = s.accept()    
        print ('Got connection from', addr )
        query="SELECT * FROM manager WHERE ID in ("+data[:-1]+")"
        mycursor.execute(query)
        result=mycursor.fetchall()
        print(result)
        query1="SELECT Column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='manager' ORDER BY ORDINAL_POSITION"
        mycursor.execute(query1)
        result1=mycursor.fetchall()
        print(result1)
        l=dict()
        for i in range(len(result1)):
            l[result1[i][0]]=[]
            for j in range(len(result)):
                l[result1[i][0]].append(result[j][i])
        print(l)
        l=json.dumps(l)
        c.send(l.encode())
        c.close()
        break
    tables_names = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='manager'"
    mycursor.execute(tables_names)
    tables = mycursor.fetchall()
    myresult = []
    columns = []
    for i in tables:
        names = "SELECT * FROM "+i[0]
        mycursor.execute(names)
        myresult.append(mycursor.fetchall())
        names = "SELECT Column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= '" + \
            i[0]+"' ORDER BY ORDINAL_POSITION"
        mycursor.execute(names)
        columns.append(mycursor.fetchall())
    return render_template('site2.html', table=tables, column=columns, data=myresult, n=len(tables),t="",po="")

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=4002,debug=True)