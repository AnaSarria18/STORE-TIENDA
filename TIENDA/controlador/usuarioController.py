from app import app, usuarios
from flask import render_template, request, redirect, session
import yagmail
import threading

@app.route("/", methods=['GET', 'POST'])
def autenticacion():
    if request.method == 'GET':
        return render_template("frmLogin.html")
    else:
        if request.method == 'POST':
            nombre_usuario = request.form.get('txtUsuario')
            clave_usuario = request.form.get('txtContrasena')
            usuario_info = {
                "username": nombre_usuario,
                "password": clave_usuario
            }
            existe_usuario = usuarios.find_one(usuario_info)
            if existe_usuario:          
                session['usuario'] = usuario_info   
                correo = yagmail.SMTP("sarriaarceanamaria18@gmail.com", open(".password").read(),
                                      encoding='UTF-8')
                asunto_correo = "Reporte ingreso al sistema usuario"
                mensaje_correo = f"Se informa que el usuario {nombre_usuario} ha ingresado al sistema"
                           
                hilo_correo = threading.Thread(target=enviar_correo, 
                                               args=(correo, "sarriaarceanamaria18@gmail.com", asunto_correo, mensaje_correo))
                hilo_correo.start()
                return redirect("/listarProductos")
            else:
                mensaje_error = "Credenciales de ingreso no válidas"
                return render_template("frmLogin.html", mensaje=mensaje_error)
            
@app.route("/salir")
def cerrar_sesion():
    session.pop('usuario', None)
    session.clear()
    return render_template("frmLogin.html", mensaje="Ha cerrado la sesión.")

def enviar_correo(email=None, destinatario=None, asunto=None, mensaje=None):
    email.send(to=destinatario, subject=asunto, contents=mensaje)
