from datetime import datetime; from flask import Flask, render_template, redirect, request, flash, session; import os, sqlite3, utils; from sqlite3 import Error; from werkzeug.security import generate_password_hash, check_password_hash; from markupsafe import escape

app = Flask(__name__)
app.secret_key=os.urandom(24)

@app.route('/', methods=['GET','POST'])
def Login():
    if request.method == 'POST':
        user=escape(request.form['user'])
        pw=escape(request.form['pass'])
        try:
            with sqlite3.connect('database.db') as db:
                cur = db.cursor()
                data=cur.execute("SELECT clave, rol FROM Sesiones WHERE username = ?",[user]).fetchone()
                if not data is None:
                    pw_hash=data[0]
                    rol_user=data[1]
                    if check_password_hash(pw_hash,pw):
                        session['user']=user
                        session['rol']=rol_user
                        return redirect('/Inicio')
                    else:
                        flash('Contraseña incorrecta')
                else:
                    flash('Usuario invalido')
                return redirect('/')
        except Error:
            print(Error)
    return render_template('index.html')

@app.route('/Signup', methods=['GET','POST'])
def SignUP():
    if request.method == 'POST':
        email=escape(request.form['email'])
        user=escape(request.form['user'])
        pw=escape(request.form['pass'])
        pw_hash=generate_password_hash(pw)
        if not utils.isEmailValid(email):
            flash('Email invalido')
            return redirect('/Signup')
        elif not utils.isUsernameValid(user):
            flash('Usuario invalido')
            return redirect('/Signup')
        elif not utils.isPasswordValid(pw):
            flash('Contraseña invalido')
            return redirect('/Signup')
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
                    return redirect('/Signup')
        except Error:
            print(Error)
    return render_template('registro.html')

@app.route('/Inicio', methods=['GET'])
def Home():
    if 'user' in session:
        try:
            with sqlite3.connect('database.db') as db:
                cur = db.cursor()
                cur.execute("SELECT * FROM Posts ORDER BY id desc")
                dataPost=cur.fetchall()
            return render_template('front.html',user=session['user'],rol=session['rol'],    dataPost=dataPost)
        except Error:
            print(Error)
    else:
        return redirect('/')

@app.route('/Post',methods=['POST'])
def Post():
    if 'user'in session:
        global message,img,fecha
        if request.method=='POST':
            message=str(escape(request.form['text']))
            file=request.files['fileImg']
            if file.filename!='':
                img=f"static/img/{file.filename}"
                file.save(img)
            else:
                img='None'
            fecha=str(datetime.today()).split(" ")
            user=session['user']
            try:
                with sqlite3.connect('database.db') as db:
                    cur = db.cursor()
                    cur.execute("INSERT INTO Posts(username,fecha,mensage,imagen) VALUES(?,?,?,?)",(user,fecha[0],message,img))
            except Error:
                print(Error)
        return redirect('/Inicio')
    else:
        return redirect('/')

@app.route('/Post/Edit/<string:user>/<int:id>',methods=['GET','POST'])
@app.route('/Post/Delete/<string:user>/<int:id>',methods=['GET'])
def EditDelete(user,id):
    if 'user' in session:
        try:
            with sqlite3.connect('database.db') as db:
                cur = db.cursor()
                if request.path==f'/Post/Edit/{user}/{id}' and (session['rol']!='USUARIO' or user==session['user']):
                    if request.method=='POST':
                        message=str(escape(request.form['text']))
                        file=request.files['fileImg']
                        fecha=str(datetime.today()).split(" ")
                        if file.filename!='':
                            img=f"static/img/{file.filename}"
                            file.save(img)
                            cur.execute("UPDATE Posts SET mensage=?, imagen=?, fecha=? WHERE id = ?",(message,img,fecha[0],id))
                        else:
                            img=cur.execute("SELECT imagen FROM Posts WHERE id = ?",[id]).fetchone()
                            cur.execute("UPDATE Posts SET mensage=?, imagen=?, fecha=? WHERE id = ?",(message,img[0],fecha[0],id))
                        return redirect('/Inicio')
                    data=cur.execute("SELECT * FROM Posts WHERE id = ?",[id]).fetchone()
                    return render_template('editPost.html',data=data)
                elif request.path==f'/Post/Delete/{user}/{id}' and (session['rol']!='USUARIO' or user==session['user']):
                    cur.execute("DELETE FROM Posts WHERE id = ?",[id])
                    return redirect('/Inicio')
                else:
                    return redirect('/Inicio')
        except Error:
            print(Error)
    else:
        return redirect('/')  

@app.route('/User/<username>', methods=['GET'])
def Profile(username):
    if 'user' in session:
        try:
            with sqlite3.connect('database.db') as db:
                db.row_factory=sqlite3.Row
                cur = db.cursor()
                dataUser=cur.execute("SELECT username,email,pais,ciudad,telefono,descripcion FROM Sesiones WHERE username = ?",[username]).fetchone()
                dataFotos=cur.execute("SELECT imagen FROM Posts WHERE username = ?",[username]).fetchall()
                if not dataUser:
                    return f"Usuario {username} no encntrado"
                return render_template('user.html',username=username,user=session['user'],rol=session['rol'],dataUser=dataUser,dataFotos=dataFotos, dataFotoslen=len(dataFotos))
        except Error:
            print(Error)
    else:
        return redirect('/')

@app.route('/User/<username>/Edit', methods=['POST'])
def ProfileEdit(username):
    if 'user' in session:
        if request.method=='POST':
            if username==session['user']:
                desc=request.form['desc']
                pais=request.form['pais']
                ciud=request.form['ciud']
                tel=request.form['tel']
                user=request.form['user']
                email=request.form['email']
                try:
                    with sqlite3.connect('database.db') as db:
                        cur = db.cursor()
                        userUse=cur.execute("SELECT username FROM Sesiones WHERE username = ?",[user]).fetchone()
                        if userUse!=None:
                            print("si")
                            user=session['user']
                        if user==session['user']:
                            cur.execute("UPDATE Sesiones SET email=?,descripcion=?,pais=?,ciudad=?,telefono=? WHERE username=?",(email,desc,pais,ciud,tel,session['user']))
                        else:
                            cur.execute("UPDATE Sesiones SET email=?,username=?,descripcion=?,pais=?,ciudad=?,telefono=? WHERE username=?",(email,user,desc,pais,ciud,tel,session['user']))
                            cur.execute("UPDATE Posts SET username  = ? WHERE username=?",(user,session['user']))
                            session['user']=user
                        return redirect(f"/User/{session['user']}")
                except Error:
                    print(Error)
        return redirect('/Inicio')
    else:
        return redirect('/')

@app.route('/User/<username>/Delete', methods=['GET'])
def ProfileDelete(username):
    if 'user' in session:
        if session['rol']!='USUARIO':
            try:
                with sqlite3.connect('database.db') as db:
                    cur= db.cursor()
                    cur.execute("DELETE FROM Posts WHERE username = ?",[username])
                    cur.execute("DELETE FROM Sesiones WHERE username = ?",[username])
                    return redirect('/Dash')
            except Error:
                print(Error)
        else:
            return redirect('/Inicio')
    else:
        return redirect('/')

@app.route('/Dash', methods=['GET'])
def Dash():
    if 'user' in session:
        try:
            with sqlite3.connect('database.db') as db:
                cur = db.cursor()
                dataPost=cur.execute("SELECT * FROM Posts WHERE username = ? ORDER BY id desc",[session['user']])
                if dataPost==None:
                    dataPost='None'
        except Error:
            print(Error)
        return render_template('dash.html',user=session['user'],rol=session['rol'],dataPost=dataPost)
    else:
        return redirect('/')

@app.route('/Dash/Post', methods=['GET','POST'])
def DashPost():
    if 'user' in session:
        if request.method=='POST':
            try:
                id_post=int(escape(request.form['consulta']))
            except:
                return redirect('/Dash')
            try:
                with sqlite3.connect('database.db') as db:
                    cur = db.cursor()
                    dataPost=cur.execute("SELECT * FROM Posts WHERE id = ?",[id_post]).fetchone()
                    if dataPost==None:
                        print("si es none")
                        dataPost='None'
                    return render_template('dashPost.html',user=session['user'],rol=session['rol'],dataPost=dataPost)
            except Error:
                print(Error)
        return redirect('/Dash')
    else:
        return redirect('/')

@app.route('/Dash/User', methods=['GET','POST'])
def DashUser():
    if 'user' in session:
        if request.method=='POST':
            user=request.form['consulta']
            if user==session['user']:
                return redirect('/Dash')
            try:
                with sqlite3.connect('database.db') as db:
                    cur = db.cursor()
                    dataUser=cur.execute("SELECT username,descripcion,rol FROM Sesiones WHERE username = ?",[user]).fetchone()
                    dataPost=cur.execute("SELECT * FROM Posts WHERE username = ? ORDER BY id desc",[user]).fetchall()
                    if not dataPost:
                        dataPost='None'
                        print("noo")
                    if dataUser==None:
                        dataUser='None'
                    return render_template('dashUser.html',user=session['user'],rol=session['rol'],dataUser=dataUser,dataPost=dataPost)
            except Error:
                print(Error)
            return redirect('/Dash')
        return redirect('/Dash')
    else:
        return redirect('/')

@app.route('/Dash/User/Rol/<rol>', methods=['POST'])
def ProfileRol(rol):
    if 'user' in session:
        if request.method=='POST':
            usuario=request.form['user']
            if session['rol']=='SUPERADMINISTRADOR':
                if rol=='USUARIOO' or rol=='ADMINISTRADOR' or rol=='SUPERADMINISTRADOR':
                    try:
                        with sqlite3.connect('database.db') as db:
                            cur= db.cursor()
                            cur.execute("UPDATE Sesiones SET rol = ? WHERE username = ?",(rol,usuario))
                            return redirect('/Dash')
                    except Error:
                        print(Error)
        return redirect('/Dash')
    else:
        return redirect('/')

@app.route('/Search', methods=['GET','POST'])
def Search():
    if 'user' in session:
        return render_template('search.html',user=session['user'],rol=session['rol'])
    else:
        return redirect('/')

@app.route('/Logout', methods=['GET'])
def Logout():
    if 'user' in session:
        session.popitem()
    return redirect('/')  

if __name__=='__main__':
    app.run( host='0.0.0.0', port=443, ssl_context=('micertificado.pem', 'llaveprivada.pem'), debug=True)