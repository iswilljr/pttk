from flask import Flask, render_template, redirect, request
from flask.helpers import flash
import os
app = Flask(__name__)
app.secret_key=os.urandom(24)

logged=False
users=['123']
passwords=['123']

@app.route('/', methods=['GET','POST'])
def Index():
    return render_template('index.html')

@app.route('/Login', methods=['GET','POST'])
def Login():
    global logged
    if request.method == 'POST':
        user=request.form['user']
        passw=request.form['pass']
        if user=='123' and passw=='123':
            logged=True
            return redirect('/Inicio')
        else:
            flash("Usuario o contraseña invalido")
            return render_template('index.html')


@app.route('/SignUp', methods=['GET','POST'])
def SignUP():
    return render_template('registro.html')

@app.route('/Sign', methods=['GET','POST'])
def Sign():
    flash("Ya estás registrado, ¡Inicia sesión!")
    return redirect('/')

@app.route('/Inicio', methods=['GET'])
def Home():
    if logged:
        return render_template('front.html')
    else:
        flash("Inicia sesión prueba con 123 y 123, o registrate")
        return redirect('/')

@app.route('/User/<user>', methods=['GET','POST'])
def Profile(user):
    if logged:
        return render_template('user.html',user=user)
    else:
        flash("Inicia sesión prueba con 123 y 123, o registrate")
        return redirect('/')

@app.route('/Dash', methods=['GET','POST'])
def Dash():
    if logged:
        return render_template('dash.html')
    else:
        flash("Inicia sesión prueba con 123 y 123, o registrate")
        return redirect('/')

@app.route('/Search', methods=['GET'])
def Search():
    if logged:
        return render_template('search.html')
    else:
        flash("Inicia sesión prueba con 123 y 123, o registrate")
        return redirect('/')

if __name__=='__main__':
    app.run(debug=True,port=8000,host='0.0.0.0')

