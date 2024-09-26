from flask import Flask
from flask_cors import CORS
import pymongo
import pymongo.errors


app = Flask(__name__)
CORS(app)
app.secret_key = '1058964416'  
app.config['UPLOAD_FOLDER'] = './static/imagenes'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

miconexion = pymongo.MongoClient('mongodb+srv://maria:ana123@cluster0.q92cait.mongodb.net/Tienda?retryWrites=true&w=majority&appName=Cluster0')
baseDatos = miconexion["Tienda"]
usuarios = baseDatos["usuario"]
productos = baseDatos["producto"]


if __name__ == "__main__":
    from controllers.usuarioController  import *
    from controllers.productosController import *
    app.run(port=5000, debug=True)


""" el usuario y la contraseña para poder ingresar son ; 
usuario: ana
contraseña: 12345 """