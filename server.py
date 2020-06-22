import os, json
from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for
from flask_mysqldb import MySQL



app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'usuarios'
mysql = MySQL(app)


#ruta principal
@app.route('/')
def index():
    #RECIVIMOS LOS DATOS DE MYSQL
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuario')
    #LOS GUARDAMOS EN UNA VARIABLE
    datos = cursor.fetchall()
    return render_template('index.html', data = datos)

#RUTA PARA AGREGAR USUARIO
@app.route('/add', methods=['POST'])
def formulario():
    if request.method == "POST":
        #RECIVIMOS LOS DATOS DEL FORMULARIO
        nombre = request.form['nombre']
        email = request.form['email']
        #LOS GUARDAMOS EN LA BASE DE DATOS
        cursor = mysql.connection.cursor()
        cursor.execute(f'INSERT INTO usuario (nombre, email) VALUES ("{nombre}", "{email}")')
        mysql.connection.commit()
         
        
    return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def Eliminar(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'DELETE FROM usuario WHERE id = {id}')
    mysql.connection.commit()
    return redirect(url_for('index'))



@app.route('/edit/<string:id>')
def Editar(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'SELECT * FROM usuario WHERE id = {id}')
    datos = cursor.fetchall()
    return render_template('usuario.html', data = datos)

@app.route('/update/<string:id>', methods=['POST'])
def actualizar(id):
    if request.method == "POST":
        #RECIVIMOS LOS DATOS DEL FORMULARIO
        nombre = request.form['nombre']
        email = request.form['email']
        print(nombre, email, id)
        #Actualizamos el dato
        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE usuario 
                            SET nombre = %s,
                            email = %s 
                        WHERE id = %s
                    """, (nombre, email, id))
        mysql.connection.commit()
    return redirect(url_for('index'))

@app.route('/buscar', methods=['POST'])
def Busacar():
    nombre = request.form['nombre']
    cursor = mysql.connection.cursor()
    cursor.execute(f'SELECT * FROM usuario WHERE nombre = "{nombre}"')
    datos = cursor.fetchall()
    print(datos)
    return jsonify(datos)

#obtener los datos en formato json
@app.route('/getDataJson')
def getData():
    #RECIVIMOS LOS DATOS DE MYSQL
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuario')
    #LOS GUARDAMOS EN UNA VARIABLE
    datos = cursor.fetchall()
    objeto = {'datos': datos}
    return jsonify(objeto)

if __name__ == '__main__':
    app.run(debug=True, port=3000)