from datetime import datetime
from flask import Flask, render_template, redirect, request, flash, session
import os, sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape

app = Flask(__name__)
app.secret_key=os.urandom(24)

@app.route('/', methods=['GET','POST'])
def Login():
    if request.method == 'POST':
        user=escape(request.form['user'])
        pw=escape(request.form['pass'])
        try:
            with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                cur = db.cursor()
                data=cur.execute("SELECT clave, rol FROM Sesiones WHERE username = ?",[user]).fetchone()
                if not data is None:
                    pw_hash=data[0]
                    rol_user=data[1]
                    if check_password_hash(pw_hash,pw):
                        session['user']=user
                        session['rol']=rol_user
                        session['rdct']='/Inicio'
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
def Signup():
    if request.method == 'POST':
        email=escape(request.form['email'])
        user=escape(request.form['user'])
        pw=escape(request.form['pass'])
        pw_hash=generate_password_hash(pw)
        try:
            with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
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
        session['rdct']="/Inicio"
        try:
            with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                cur = db.cursor()
                dataPost=cur.execute("SELECT * FROM Posts ORDER BY id desc").fetchall()
                dataComt=cur.execute("SELECT * FROM Comentarios").fetchall()
            return render_template('front.html',user=session['user'],rol=session['rol'],dataPost=dataPost,dataComt=dataComt)
        except Error:
            print(Error)
    else:
        return redirect('/')

@app.route('/Post',methods=['POST'])
def Post():
    if 'user' in session:
        if request.method=='POST':
            message=str(escape(request.form['text']))
            file=request.files['fileImg']
            if file.filename!='':
                img=f"/home/WillJr/mysite/static/img/{file.filename}"
                file.save(img)
            else:
                img='None'
            fecha=str(datetime.today()).split(" ")
            user=session['user']
            try:
                with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                    cur = db.cursor()
                    cur.execute("INSERT INTO Posts(username,fecha,mensaje,imagen) VALUES(?,?,?,?)",(user,fecha[0],message,img))
                    flash("¡Subido con éxito!")
            except Error:
                print(Error)
        return redirect('/Inicio')
    else:
        return redirect('/')

@app.route('/Post/Comentario', methods=['POST'])
def PostComt():
    if 'user' in session:
        if request.method=='POST':
            id_post=int(escape(request.form['id_post']))
            destino=escape(request.form['destino'])
            username=escape(session['user'])
            comentario=escape(request.form['comentario'])
            try:
                with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                    cur = db.cursor()
                    cur.execute("INSERT INTO Comentarios(id_post,username,comentario,destino)VALUES(?,?,?,?)",(id_post,username,comentario,destino))
                    flash("Mensaje comentado")
                    return redirect(f"{session['rdct']}#{id_post}")
            except Error:
                print(Error)
        return redirect(f"{session['rdct']}#{id_post}")
    else:
        return redirect('/')

@app.route('/Post/Comentario/Edit', methods=['POST'])
def PostComEdit():
    if 'user' in session:
        if request.method=='POST':
            id_post=int(escape(request.form['id_post']))
            id_comt=int(escape(request.form['id-comt-post']))
            comentario=escape(request.form['post-comt-edit'])
            try:
                with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                    cur = db.cursor()
                    cur.execute("UPDATE Comentarios SET comentario = ? WHERE id_comt = ?",(comentario,id_comt))
                    flash("Comentario actualizado")
                    return redirect(f"{session['rdct']}#{id_post}")
            except Error:
                print(Error)
        return redirect(session['rdct'])
    else:
        return redirect('/')

@app.route('/Post/Comentario/Delete/<id>', methods=['GET'])
def PostComtDelt(id):
    if 'user' in session:
        try:
            with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                cur = db.cursor()
                comp=cur.execute("SELECT username,destino FROM Comentarios WHERE id_comt = ?",[id]).fetchone()
                if session['user']==comp[0] or session['user']==comp[1] or session['rol']!='USUARIO':
                    cur.execute("DELETE FROM Comentarios WHERE id_comt= ?",[id])
                    flash("Comentario eliminado")
                return redirect(session['rdct'])
        except Error:
            print(Error)
        return redirect(session['rdct'])
    else:
        return redirect('/')

@app.route('/Post/Edit/<string:user>/<int:id>',methods=['GET','POST'])
@app.route('/Post/Delete/<string:user>/<int:id>',methods=['GET'])
def EditDelete(user,id):
    if 'user' in session:
        try:
            with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                cur = db.cursor()
                if request.path==f'/Post/Edit/{user}/{id}' and (session['rol']!='USUARIO' or user==session['user']):
                    if request.method=='POST':
                        message=str(escape(request.form['text']))
                        file=request.files['fileImg']
                        fecha=str(datetime.today()).split(" ")
                        if file.filename!='':
                            img=f"/home/WillJr/mysite/static/img/{file.filename}"
                            file.save(img)
                            cur.execute("UPDATE Posts SET mensaje=?, imagen=?, fecha=? WHERE id = ?",(message,img,fecha[0],id))
                        else:
                            img=cur.execute("SELECT imagen FROM Posts WHERE id = ?",[id]).fetchone()
                            cur.execute("UPDATE Posts SET mensaje=?, imagen=?, fecha=? WHERE id = ?",(message,img[0],fecha[0],id))
                        flash("Post actualizado")
                        return redirect(session['rdct'])
                    data=cur.execute("SELECT * FROM Posts WHERE id = ?",[id]).fetchone()
                    return render_template('layouts/post/editPost.html',data=data)
                elif request.path==f'/Post/Delete/{user}/{id}' and (session['rol']!='USUARIO' or user==session['user']):
                    cur.execute("DELETE FROM Posts WHERE id = ?",[id])
                    cur.execute("DELETE FROM Comentarios WHERE id_post = ?",[id])
                    flash("Post eliminiado")
                    return redirect(session['rdct'])
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
            with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
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
            if session['rol']!='USUARIO' or username==session['user']:
                desc=request.form['desc']
                pais=request.form['pais']
                ciud=request.form['ciud']
                tel=request.form['tel']
                user=request.form['user']
                email=request.form['email']
                try:
                    with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                        cur = db.cursor()
                        if user!=username:
                            userUse=cur.execute("SELECT username FROM Sesiones WHERE username = ?",[user]).fetchone()
                            if userUse!=None:
                                user=username
                                flash("Usuario en uso")
                            else:
                                cur.execute("UPDATE Posts SET username = ? WHERE username = ?",(user,username))
                        cur.execute("UPDATE Sesiones SET email=?,username=?,descripcion=?,pais=?,ciudad=?,telefono=? WHERE username=?",(email,user,desc,pais,ciud,tel,username))
                        flash("Perfil actualizado")
                        if username==session['user']:
                            session['user']=user
                            return redirect(f"/User/{session['user']}")
                        return redirect(f"/User/{user}")
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
                with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                    cur= db.cursor()
                    cur.execute("DELETE FROM Comentarios WHERE username = ?",[username])
                    cur.execute("DELETE FROM Posts WHERE username = ?",[username])
                    cur.execute("DELETE FROM Sesiones WHERE username = ?",[username])
                    flash("Usuario eliminado")
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
        session['rdct']="/Dash"
        try:
            with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                cur = db.cursor()
                dataPost=cur.execute("SELECT * FROM Posts WHERE username = ? ORDER BY id desc",[session['user']]).fetchall()
                dataComt=cur.execute("SELECT * FROM Comentarios WHERE destino = ? or username = ?",(session['user'],session['user'])).fetchall()
        except Error:
            print(Error)
        return render_template('dash.html',user=session['user'],rol=session['rol'],dataPost=dataPost,dataComt=dataComt)
    else:
        return redirect('/')

@app.route('/Dash/Post', methods=['GET'])
def DashPost():
    if 'user' in session:
        if session['rol']!='USUARIO':
            consulta=escape(request.args.get('consulta'))
            if consulta is None:
                pass
            else:
                try:
                    with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                        cur = db.cursor()
                        dataPost=cur.execute("SELECT * FROM Posts WHERE id = ?",[consulta]).fetchone()
                        dataComt=cur.execute("SELECT * FROM Comentarios WHERE id_post = ?",[consulta]).fetchall()
                        if dataPost==None:
                            dataPost='None'
                        try:
                            consulta=int(consulta)
                        except:
                            return redirect('/Dash')
                        return render_template('layouts/dash/dashPost.html',user=session['user'],rol=session['rol'],dataPost=dataPost,dataComt=dataComt,consulta=consulta)
                except Error:
                        print(Error)
        return redirect('/Dash')
    else:
        return redirect('/')

@app.route('/Dash/User', methods=['GET'])
def DashUser():
    if 'user' in session:
        consulta=escape(request.args.get('consulta'))
        if consulta=="":
            pass
        else:
            if consulta!=session['user'] and session['rol']!='USUARIO':
                try:
                    with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                        cur = db.cursor()
                        dataUser=cur.execute("SELECT username,descripcion,rol FROM Sesiones WHERE username = ?",[consulta]).fetchone()
                        dataPost=cur.execute("SELECT * FROM Posts WHERE username = ? ORDER BY id desc",[consulta]).fetchall()
                        dataComt=cur.execute("SELECT * FROM Comentarios WHERE username = ?",[consulta]).fetchall()
                        if not dataPost:
                            dataPost='None'
                        if dataUser==None:
                            dataUser='None'
                        return render_template('layouts/dash/dashUser.html',user=session['user'],rol=session['rol'],dataUser=dataUser,dataPost=dataPost,dataComt=dataComt,consulta=consulta)
                except Error:
                    print(Error)
        return redirect('/Dash')
    else:
        return redirect('/')

@app.route('/Dash/User/Rol/<rol>', methods=['POST'])
def ProfileRol(rol):
    if 'user' in session:
        if request.method=='POST':
            usuario=request.form['user']
            if session['rol']=='SUPERADMINISTRADOR':
                if rol=='USUARIO' or rol=='ADMINISTRADOR' or rol=='SUPERADMINISTRADOR':
                    try:
                        with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                            cur= db.cursor()
                            cur.execute("UPDATE Sesiones SET rol = ? WHERE username = ?",(rol,usuario))
                            flash("Rol cambiado con éxito")
                            return redirect('/Dash')
                    except Error:
                        print(Error)
        return redirect('/Dash')
    else:
        return redirect('/')


@app.route('/Search', methods=['GET'])
def Search():
    if 'user' in session:
        consulta=request.args.get('search')
        consulta= consulta + "%"
        consulta2= "%" + consulta
        if consulta is None or consulta=="":
            busqueda="None"
        else:
            try:
                with sqlite3.connect('/home/WillJr/mysite/database.db') as db:
                    cur = db.cursor()
                    busqueda=cur.execute("SELECT username,descripcion FROM Sesiones WHERE username LIKE ?",[consulta]).fetchall()
                    posts=cur.execute("SELECT * FROM Posts WHERE mensaje LIKE ? ORDER BY id desc",[consulta2]).fetchall()
                    dataComt=cur.execute("SELECT * FROM Comentarios").fetchall()
                    print(posts)
                    print(dataComt)
            except Error:
                print(Error)
        return render_template('search.html',user=session['user'],rol=session['rol'],busqueda=busqueda,posts=posts,dataComt=dataComt)
    else:
        return redirect('/')

@app.route('/Logout', methods=['GET'])
def Logout():
    if 'user' in session:
        session.popitem()
    return redirect('/')