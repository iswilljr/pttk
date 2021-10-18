from flask import Flask, render_template, redirect, request, flash, session
import os, sqlite3, utils
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape

app = Flask(__name__)
app.secret_key=os.urandom(24)

@app.route('/', methods=['GET','POST'])
def Index():
    return render_template('index.html')

@app.route('/Login', methods=['GET','POST'])
def Login():
    global user, rol
    if request.method == 'POST':
        user=escape(request.form['user'])
        pw=escape(request.form['pass'])
        try:
            with sqlite3.connect('database.db') as db:
                cur = db.cursor()
                data=cur.execute("SELECT clave, rol FROM Sesiones WHERE username = ?",[user]).fetchone()
                if not data is None:
                    pw_hash=data[0]
                    rol=data[1]
                    if check_password_hash(pw_hash,pw):
                        session['user']=user
                        return redirect('/Inicio')
                    else:
                        flash('Contraseña incorrecta')
                else:
                    flash('Usuario invalido')
                return redirect('/')                
        except Error:
            print(Error)
    return redirect('/')

@app.route('/SignUp', methods=['GET','POST'])
def SignUP():
    return render_template('registro.html')

@app.route('/Sign', methods=['GET','POST'])
def Sign():
    if request.method == 'POST':
        email=escape(request.form['email'])
        user=escape(request.form['user'])
        pw=escape(request.form['pass'])
        pw_hash=generate_password_hash(pw)
        if not utils.isEmailValid(email):
            flash('Email invalido')
            return redirect('/SignUp')
        elif not utils.isUsernameValid(user):
            flash('Usuario invalido')
            return redirect('/SignUp')
        elif not utils.isPasswordValid(pw):
            flash('Contraseña invalido')
            return redirect('/SignUp')
        try:
            with sqlite3.connect('database.db') as db:
                cur = db.cursor()
                userUse=cur.execute("SELECT username FROM Sesiones WHERE username = ?",[user]).fetchone()
                if userUse is None:
                    cur.execute("INSERT INTO Sesiones(email,username,clave) VALUES(?,?,?)",(email,user,pw_hash))
                    flash('Usuario registrado, ¡Inicia sesión!')
                    return redirect('/')
                else:
                    flash('Usuario en uso, pruebe con otro')
                    return redirect('/SignUp')
        except Error:
            print(Error)
    return redirect('/SignUp')

@app.route('/Inicio', methods=['GET'])
def Home():
    if 'user' in session:
        return render_template('front.html',user=user,rol=rol)
    else:
        return redirect('/')

@app.route('/User/<username>', methods=['GET'])
def Profile(username):
    if 'user' in session:
        print(username,user)
        return render_template('user.html',username=username,user=user,rol=rol)
    else:
        return redirect('/')

@app.route('/Dash', methods=['GET'])
def Dash():
    if 'user' in session:
        return render_template('dash.html',user=user,rol=rol)
    else:
        return redirect('/')

@app.route('/Search', methods=['GET'])
def Search():
    if 'user' in session:
        return render_template('search.html',user=user,rol=rol)
    else:
        return redirect('/')

@app.route('/Logout')
def Logout():
    if 'user' in session:
        session.popitem()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')