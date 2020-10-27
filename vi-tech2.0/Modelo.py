from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL

 
app = Flask(__name__)
 
app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'sepherot_javier'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Pzk6IDs4by'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_javierBD'
app.config['MYSQL_DATABASE_HOST'] = 'nemonico.com.mx'
mysql = MySQL(app)
 
def InsertName(_N, _L, _E, _P):
    try:
        _N = request.form.get('Name')
        _L = request.form.get('LastName')
        _E = request.form.get('Mail')   
        _P = request.form.get('Password')

        if _N and _L and _E and _P:
            conn = mysql.connect()
            cursor = conn.cursor()
            _TABLA="Usuarios"
            sqlDropProcedure="DROP PROCEDURE IF EXISTS InsertName;"
            cursor.execute(sqlDropProcedure)
            sqlCreateSP="CREATE PROCEDURE InsertName(IN PName VARCHAR(100), IN PLastName VARCHAR(100), IN PMail VARCHAR(50), IN PPassword VARCHAR(50)) INSERT INTO "+_TABLA+"(Name, LastName, Mail, Password) VALUES (Name, LastName, Mail, Password)"
            cursor.execute(sqlCreateSP)
            cursor.execute("CREATE TABLE IF NOT EXISTS `sepherot_javierBD`.`"+_TABLA+"` ( `ID_Usuario` INT(50) NOT NULL AUTO_INCREMENT , `Name` VARCHAR(100) NULL , `LastName` VARCHAR(100) NULL ,`Mail` VARCHAR(50) NULL ,`Password` VARCHAR(50) NULL, PRIMARY KEY (`ID_Usuario`)) ENGINE = InnoDB;")
            #cursor.execute("INSERT INTO "+_TABLA+"(Usuario, Evento) VALUES (%s, %s)", (_usuario, _evento))
            cursor.callproc('InsertName',(_N, _L, _E, _P))
            data = cursor.fetchall()
            
            if len(data)==0:
                conn.commit()
                return json.dumps({'message':'Usuario registrado!'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Datos faltantes</span>'})
            
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
            cursor.close() 
            conn.close()

def InsertarEvento(_Nombre, _TipoEvento, _NumPersonas, _Ubicación, _Fecha):
    try:
        if _Nombre and _TipoEvento and _NumPersonas and _Ubicación and _Fecha:
            conn = mysql.connect()
            cursor = conn.cursor()
            _TABLA="C_eventos"
            sqlDropProcedure="DROP PROCEDURE IF EXISTS InsertarEvento;"
            cursor.execute(sqlDropProcedure)
            sqlCreateSP="CREATE PROCEDURE InsertEvento(IN PNombre VARCHAR(100), IN PTipo_Evento VARCHAR(100), IN PNum_Personas INT(50), IN PUbicación VARCHAR(100), IN PFecha VARCHAR(50)) INSERT INTO "+_TABLA+"(Nombre, Tipo_Evento, Num_Personas, Ubicación, Fecha) VALUES (PNombre, PTipo_Evento, PNum_Personas, PUbicación, PFecha)"
            cursor.execute("CREATE TABLE IF NOT EXISTS `sepherot_javierDB`.`"+_TABLA+"` ( `ID_Evento` INT NOT NULL AUTO_INCREMENT , `Nombre` VARCHAR(100) NOT NULL , `Tipo_Evento` VARCHAR(100) NOT NULL , `Num_Personas` VARCHAR(50) NOT NULL , `Ubicación` VARCHAR(100) NOT NULL ,`Fecha` VARCHAR(50) NOT NULL , PRIMARY KEY (`ID_Evento`)) ENGINE = InnoDB;")
            cursor.execute(sqlCreateSP)
            cursor.callproc('InsertarEvento',(_Nombre, _TipoEvento, _NumPersonas, _Ubicación, _Fecha))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'Lectura registrada correctamente !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Datos faltantes</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
       cursor.close() 
       conn.close()

def selectALLEventos():
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute('select * from C_Eventos order by ID desc')
        Eventos=cursor.fetchall()
        return Eventos
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()