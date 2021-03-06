from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL

 
app = Flask(__name__)
 
app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'sepherot_javier'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Pzk6IDs4by'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_javierBD'
app.config['MYSQL_DATABASE_HOST'] = 'nemonico.com.mx'

mysql = MySQL(app)
#mysql.init_app(app)

#conn = mysql.connect()
#if conn == True:
#    print("si se pudo")
#else:
#    print("no se pudo")


#def InsertName(_N, _L, _E, _P):
#    try:
#        if _N and _L and _E and _P:
#            conn = mysql.connect()
#            cursor = conn.cursor()
#            _TABLA="Usuarios"
#           sqlDropProcedure="DROP PROCEDURE IF EXISTS InsertName;"
#            cursor.execute(sqlDropProcedure)
#            sqlCreateSP="CREATE PROCEDURE InsertName(IN PName VARCHAR(100), IN PLastName VARCHAR(100), IN PMail VARCHAR(50), IN PPassword VARCHAR(50)) INSERT INTO "+_TABLA+"(Name, LastName, Mail, Password) VALUES (PName, PLastName, PMail, PPassword)"
#            cursor.execute(sqlCreateSP)
#            cursor.execute("CREATE TABLE IF NOT EXISTS `sepherot_javierBD`.`"+_TABLA+"` ( `ID_Usuario` INT(50) NOT NULL AUTO_INCREMENT , `Name` VARCHAR(100) NULL , `LastName` VARCHAR(100) NULL ,`Mail` VARCHAR(50) NULL ,`Password` VARCHAR(50) NULL, PRIMARY KEY (`ID_Usuario`)) ENGINE = InnoDB;")
#           #cursor.execute("INSERT INTO "+_TABLA+"(Usuario, Evento) VALUES (%s, %s)", (_usuario, _evento))
#            cursor.callproc('InsertName',(_N, _L, _E, _P))
#           data = cursor.fetchall()
#            
#            if len(data)==0:
#                conn.commit()
#                return json.dumps({'message':'Usuario registrado!'})
#            else:
#                return json.dumps({'error':str(data[0])})
#        else:
#            return json.dumps({'html':'<span>Datos faltantes</span>'})
#            
#    except Exception as e:
#        return json.dumps({'error':str(e)})
#    finally:
#            cursor.close() 
#            conn.close()  

def InsertName(_N,_L,_E,_P):
    try:           
        conn=mysql.connect()
        cursor=conn.cursor()
        _result=cursor.execute('insert into Usuarios (Name, LastName, Mail, Password) values (%s,%s,%s,%s)', (_N,_L,_E,_P))
        print(_result)
        cursor.execute(_result)
        conn.commit()
        return "success"
    except Exception as a:
            return json.dumps({'error':str(a)})
    finally:
        cursor.close() 
        conn.close() 

def InsertarEvento(_Nombre, _TipoEvento):
    try:
        if _Nombre and _TipoEvento:
            conn = mysql.connect()
            cursor = conn.cursor()
            _TABLA="C_eventos"
            sqlDropProcedure="DROP PROCEDURE IF EXISTS InsertarEvento;"
            cursor.execute(sqlDropProcedure)
            sqlCreateSP="CREATE PROCEDURE InsertEvento(IN PNombre VARCHAR(100), IN PTipo_Evento VARCHAR(100)) INSERT INTO "+_TABLA+"(Nombre, Tipo_Evento) VALUES (PNombre, PTipo_Evento)"
            cursor.execute("CREATE TABLE IF NOT EXISTS `sepherot_javierDB`.`"+_TABLA+"` ( `ID_Evento` INT NOT NULL AUTO_INCREMENT , `Nombre` VARCHAR(100) NOT NULL , `Tipo_Evento` VARCHAR(100) NOT NULL, PRIMARY KEY (`ID_Evento`)) ENGINE = InnoDB;")
            cursor.execute(sqlCreateSP)
            cursor.callproc('InsertarEvento',(_Nombre, _TipoEvento,))
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

def selectALLContratos():
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute('select * from C_Contratos order by ID desc')
        Eventos=cursor.fetchall()
        return Eventos
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

def InsertarBoda(_ConUno, _ConDos, _Lugar):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _TABLA="C_Bodas"
        sqlCreateSP="INSERT INTO "+_TABLA+"(Primer_Conyuge, Segundo_Conyuge, Lugar) VALUES (""'"+_ConUno+"'"",""'"+_ConDos+"'"",""'"+_Lugar+"'"")"
        cursor.execute(sqlCreateSP)
        data = cursor.fetchall()
        if len(data) == 0:
            conn.commit()
            return True

        else:
            return json.dumps({'error':str(data[0])})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
       cursor.close() 
       conn.close()

def InsertarXV(name, name2, date, hour):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        print("venga")
        _TABLA="C_XV"
        sqlCreateSP="INSERT INTO "+_TABLA+"(Nombre_Padres, Nombre_XV, Fecha, Hora) VALUES (""'"+name+"'"",""'"+name2+"'"",""'"+date+"'"",""'"+hour+"'"")"
        cursor.execute(sqlCreateSP)
        data = cursor.fetchall()
        print("venga más")
        if len(data) == 0:
            conn.commit()
            return True

        else:
            return json.dumps({'error':str(data[0])})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
       cursor.close() 
       conn.close()

def InsertarGrad(_NomR, _NombG, _Fecha, _Lugar, _Escul):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _TABLA="C_Graduación"
        sqlCreateSP="INSERT INTO "+_TABLA+"(Nombre_Rep, Nombre_Grad, Fecha, Lugar, Escuela) VALUES (""'"+_NomR+"'"",""'"+_NombG+"'"",""'"+_Fecha+"'"",""'"+_Lugar+"'"",""'"+_Escul+"'"")"
        cursor.execute(sqlCreateSP)
        data = cursor.fetchall()
        if len(data) == 0:
            conn.commit()
            return True

        else:
            return json.dumps({'error':str(data[0])})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
       cursor.close() 
       conn.close()


def entities(User, Stage, StageInfo, Date):
    try:
        if User and Stage and StageInfo:
            conn = mysql.connect()
            cursor = conn.cursor()
            _TABLA="Entities"
            sqlDropProcedure="DROP PROCEDURE IF EXISTS InsertEntity;"
            cursor.execute(sqlDropProcedure)
            sqlCreateSP="CREATE PROCEDURE InsertEntity (IN PUser VARCHAR(100), IN PStage VARCHAR(100), IN PStageInfo VARCHAR(100), IN PDate TIMESTAMP) INSERT INTO " +_TABLA+ " (User, Stage, StageInfo, Date) VALUES (PUser, PSatage, PStageInfo)"
            cursor.execute(sqlCreateSP)
            cursor.execute("CREATE TABLE IF NOT EXISTS `sepherot_javierBD`.`" +_TABLA+ "` ( `entityID` INT(50) NOT NULL AUTO_INCREMENT, `User` VARCHAR(50) NOT NULL, `Stage` VARCHAR(100) NOT NULL, `StageInfo` VARCHAR(100) NOT NULL, `Date` TIMESTAMP NOT NULL, PRIMARY KEY (entityID)) ENGINE = InnoDB;")
            cursor.callproc('InsertEntity',(User, Stage, StageInfo, Date))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()
                return data
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Datos faltantes</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close() 


""" def entity(User, Stage, StageInfo, Date):
    conn = mysql.connect()
    cursor = conn.cursor()
    _TABLA="Entities"
    sqlInsertI="INSERT INTO `Entities` (`entityID`, `User`, `Stage`, `StageInfo`, `Date`) VALUES (NULL, %s, %s, %s , current_timestamp())"
    try:
        done = cursor.execute(query, (User, Stage, StageInfo, Date))
        if done:
            return True
        else:
            return False
    except Exception as e:
                return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close() """