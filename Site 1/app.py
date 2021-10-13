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
    database="employee"
)
mycursor=mydb.cursor()

@app.route('/', methods=['POST', 'GET'])
def site1():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="employee"
    )
    mycursor=mydb.cursor()
    tables_names = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='employee'"
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
        temp=str(s.recv(1024).decode())
        temp=json.loads(temp)
        #print(temp)
        s.close() 
        mycursor.execute("DROP TABLE IF EXISTS TEMP")
        query="CREATE TABLE TEMP ("
        for i in temp.keys():
            query=query+' '+str(i)+' '+'VARCHAR(25)'+', '
        query=query[:-2]+');'
        mycursor.execute(query)
        query1="INSERT INTO TEMP VALUES "
        for j in range(len(temp['ID'])):
            query1=query1+'('
            for i in temp.keys():
                query1=query1+str(temp[i][j])+','
            query1=query1[:-1]+'),'
        query1=query1[:-1]+';'
        mycursor.execute(query1)
        poss=""
        temp6=""
        for i in temp.keys():
            if(str(i)=='ID'):
                continue
            temp6=temp6+str(i)
            poss=poss+'TEMP.'+str(i)+', '
        poss=poss[:-2]
        query2='SELECT EMPLOYEE.*,'+poss+' FROM EMPLOYEE INNER JOIN TEMP ON EMPLOYEE.EMP_ID=TEMP.ID'
        mycursor.execute(query2)
        result=mycursor.fetchall()
        print(result)
        query3 = "SELECT Column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= '" +'employee'+"' ORDER BY ORDINAL_POSITION"
        mycursor.execute(query3)
        temp1=str()
        poss=temp6
        for i in mycursor.fetchall():
            temp1=temp1+str(i[0])+','
        poss=temp1[:-1]+','+poss
        print(poss)
        mycursor.execute("DROP TABLE TEMP")
        print(result,poss.split(','),len(result[0]))
        return render_template('site1.html', table=[], column=[], data=[], n=0,temp=temp,lop=len(temp['ID']),result=result,poss=poss.split(','),num=len(result[0]))
    except Exception as e:
        print(e)
        return render_template('site1.html', table=tables, column=columns, data=myresult, n=len(tables),temp={},lop=0,result=[],poss=[],num=0)
    #return render_template("server.html")

@app.route('/site1_work', methods=['POST', 'GET'])
def site1_work():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="employee"
    )
    s = socket.socket()
    print ("Socket successfully created")
    s.bind(('', 12345))
    print ("socket binded to %s" %(12345))
    s.listen(5)    
    print ("socket is listening")  
    while True:
        c, addr = s.accept()    
        print ('Got connection from', addr )
        query="SELECT EMP_ID FROM EMPLOYEE"
        mycursor.execute(query)
        result=mycursor.fetchall()
        temp=str()
        for i in result:
            temp=temp+str(i[0])+','
        print("Sending data",temp)
        c.send("EMP_ID".encode())
        c.send(temp.encode())
        c.close()
        break
    tables_names = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='employee'"
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
    return render_template('site1.html', table=tables, column=columns, data=myresult, n=len(tables),temp={},lop=0,result=[],poss=[],num=0)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=4001,debug=True)