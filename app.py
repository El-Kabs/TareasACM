import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route("/tareas", methods=["GET", "POST"])
def agregarTarea():
    connt = sqlite3.connect('tareas.db')
    c = connt.cursor()
    if(request.method=='POST'):
        data = request.form['text']
        if(data==''):
            retorno = ''
            c.execute("SELECT * FROM tareas")
            rows = c.fetchall()
            for x in rows:
                if(x[2]==''):
                    retorno = retorno + str(x[0])+',' + str(x[1])+',sin usuarios.' + "\n"
                else:
                    retorno = retorno + str(x[0])+',' + str(x[1])+','+ str(x[2]) + "\n"
            return retorno
        else:
            arr = data.split(':')
            if(arr[0]=='agregar'):
                tarea = arr[1]
                c.execute("INSERT INTO tareas(tarea, usuarios) VALUES (?, '')", (tarea,))
                connt.commit()
                return "Tarea: "+str(tarea)+" fue agregada."
            elif(arr[0]=='asignar'):
                usuario = arr[1]
                tarea = arr[2]
                c.execute("SELECT * FROM tareas WHERE id = ?", (tarea,))
                rows = c.fetchall()
                usuarios = ""
                for x in rows:
                    usuarios = str(x[2]).replace(' ', '')
                usuariosN = usuarios +":"+usuario
                c.execute("UPDATE tareas SET usuarios = ? WHERE id=?", (usuariosN,tarea))
                connt.commit()
                return "Usuario: "+str(usuario)+" agregado a la tarea: "+str(tarea)+"."
            elif(arr[0]=='ver'):
                usuario = arr[1]
                c.execute("SELECT * FROM tareas")
                retorno = ''
                rows = c.fetchall()
                for x in rows:
                    if(usuario in x[2]):
                        retorno = retorno + str(x[0])+',' + str(x[1])+',' + str(x[2]) + "\n"
                return retorno
            elif(arr[0]=='eliminar'):
                tarea=arr[1]
                c.execute("DELETE FROM tareas WHERE id = ?", (tarea,))
                connt.commit()
                return "Tarea: "+str(tarea)+" eliminada."
    connt.close()

if __name__ == '__main__':
    app.run(debug=True)
