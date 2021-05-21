"""
Created on Fri Jan 30 2021

@author: Harish_3055
Project Name :- bSafe 
"""
import flask
from flask import Flask, request, render_template
import sqlite3
def update(mob_send,mob_rec,amount):
    conn=sqlite3.connect('/home/runner/SparksIntern/Database/Customer.db')
    query_send="select Balance from customer where Mobile_number={}".format(mob_send)
    bal_send=[i[0] for i in conn.execute(query_send)][0]
    query_rec="select Balance from customer where Mobile_number={}".format(mob_rec)
    bal_rec=[i[0] for i in conn.execute(query_rec)][0]
    bal_send=bal_send-amount
    bal_rec=bal_rec+amount
    query="update customer set Balance={bal} where Mobile_number={no}".format(bal=bal_send,no=mob_send)
    conn.execute(query)
    query="update customer set Balance={bal} where Mobile_number={no}".format(bal=bal_rec,no=mob_rec)
    conn.execute(query)
    conn.commit()
sender_details= None 
lis=None
send_detail=None
rec_detail=None
value=None
sender_name=None
rec_name=None
app=Flask(__name__)
@app.route('/',methods=['GET'])
def customer():
    conn=sqlite3.connect('/home/runner/SparksIntern/Database/Customer.db')
    ls=[]
    for i in conn.execute("select * from customer"):
        ls.append(i)
    global lis
    lis=ls
    return render_template('customer.html',leng=len(ls),pred=ls,det='Sender',link='/customer/details/')
@app.route('/customer/details/<index>',methods=['GET'])
def details(index):
  conn=sqlite3.connect('/home/runner/SparksIntern/Database/Customer.db')
  ls=[]
  for i in conn.execute("select * from customer"):
        ls.append(i)
  global lis 
  lis=ls
  i=ls[int(index)]
  global send_detail
  send_detail = i[1]
  global sender_name
  sender_name=i[0]
  return render_template('Amount.html',i=i,index=index)
  
@app.route('/customer/Receiver_select/details/<index>/<val>')
def sender_select(index,val):
  global value
  value=val
  global sender_details
  conn=sqlite3.connect('/home/runner/SparksIntern/Database/Customer.db')
  ls=[]
  for i in conn.execute("select * from customer"):
      ls.append(i)
  sender_details=ls[int(index)]
  ls.pop(int(index))
  global lis
  lis=ls
  return render_template('customer.html',leng=len(ls),pred=ls,det='Receiver',link='/customer/details/receiver/')
@app.route('/customer/details/receiver/<index>',methods=['GET'])
def receiver_details(index):
  global lis
  i=lis[int(index)]
  global rec_detail
  rec_detail = i[1]
  global rec_name
  rec_name =i[0]
  return render_template('/sender_details.html',i=i)
@app.route('/customer/History')
def history():
  global send_detail
  global rec_detail
  global value
  global sender_name
  global rec_name
  print(send_detail,rec_detail,value)
  update(send_detail,rec_detail,int(value))
  conn=sqlite3.connect('/home/runner/SparksIntern/Database/Transaction.db')
  query = "insert into history values(?,?,?)"
  val = (sender_name,rec_name,int(value))
  conn.execute(query,val)
  conn.commit()
  ls=[]
  for i in conn.execute('select * from history'):
    ls.append(i)
  return render_template('History.html',leng=len(ls),pred=ls,link='/')
@app.route('/customer/End')
def End():
  return render_template('end.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)