from flask import Flask,render_template,request,jsonify,redirect,session
import psycopg2 
from psycopg2 import sql
import os
app=Flask(__name__)
app.secret_key =os.urandom(24)

try:
    connection = psycopg2.connect(
        user='postgres',
        password='password',
        host='127.0.0.1',
        port='5432',
        database='userpy'
    )
    cursor = connection.cursor()
    print("Database connected Successfully")
except (Exception , psycopg2.Error)as error:
    print(f'Error while connecting to Postgresql {error}')


@app.route('/Register')
def Register():
    return render_template('register.html')

@app.route('/')
def About():
    return render_template('login.html')

@app.route('/Validation', methods=['POST'])
def Validation():
    email = request.form.get('email')
    password = request.form.get('password')
    query = sql.SQL("SELECT * FROM register WHERE email = %sAND password = %s")
    cursor.execute(query,(email,password))
    users = cursor.fetchall()
    print("Users :" , users)
    if users:
        session['user_id'] = users[0][4]  
        return redirect('/Home')
    else:
        return redirect('/')
@app.route('/add_user',methods=['POST'])
def add_user():
    name = request.form.get('name')
    contact = request.form.get('contact')
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        query = sql.SQL("INSERT INTO register(name,contact,email,password) VALUES (%s,%s,%s,%s)")
        cursor.execute(query,(name,contact,email,password))
        connection.commit()
        return jsonify({'Message':"User registerd successfully"})
    except:
        return jsonify({'Error',"Failed to register user"})

@app.route('/Home')
def Home():
    if 'user_id'in session:
        return render_template('home.html')
    else:
        return redirect('/')
    
@app.route('/logout')
def Logout():
    session.pop('user_id')
    return redirect('/')
    
if __name__=="__main__":
    app.run(debug=True)