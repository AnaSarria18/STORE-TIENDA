from app import app, productos
from flask import request, jsonify, redirect,render_template, session, Response
import pymongo
import os
import pymongo.errors
from bson import json_util,ObjectId
import json


@app.route("/mostrarArticulos")
def inicioSesion():
    if("user" in session):
        return render_template("listarProductos.html")
    else:
        mensaje="ingresar con sus credenciales"
        return render_template("frmLogin.html", mensaje=mensaje)

@app.route("/api/agregarArticulo", methods=['POST'])
def apiAgregarArticulo():    
    codigo = int(request.json['codigo'])          
    nombre_articulo = request.json['nombre']
    precio_articulo = int(request.json['precio'])
    categoria_articulo = request.json['categoria']
    imagen_articulo = request.json['foto']
    
    producto = {   "codigo": codigo, "nombre": nombre_articulo, "precio": precio_articulo, 
            "categoria": categoria_articulo, "foto": imagen_articulo
        }  
    existe = verificarexistenciaProducto(codigo)
    if (not existe):   
        respuesta = productos.insert_one (producto)    
        if(respuesta.acknowledged):
            mensaje=f"Producto Agregado Correctamente"                
        else:
            mensaje="dificultad al agregar el producto."   
    else:
        mensaje=f"Ya existe un producto con el código {codigo}" 
        
    retorno = {"mensaje":mensaje}
    return jsonify(retorno)

@app.route("/api/mostrarArticulos", methods=['GET'])
def apiMostrarArticulos():
    data = productos.find()
    resultado = json_util.dumps(data)
    return jsonify(resultado)
    

@app.route("/api/consultarArticulo/<id>",methods=['GET'])
def apiConsultarArticulosPorId(id):
    data = productos.find_one({'_id':ObjectId(id)})
    if(data):
        resultado = json_util.dumps(data)
    else:
        resultado="Producto no existe con ese código"
    return Response(resultado,mimetype='application/json')
     

@app.route("/api/actualizarArticulo/<id>", methods=['PUT'])
def apiActualizarArticulo(id):
    mensaje=None
    data = request.get_json()
    respuesta = productos.update_one({'_id':ObjectId(id)},{'$set':data})
    if respuesta.modified_count >=1:
        resultado='Producto actualizado correctamente'
    else:
        resultado='Producto no encontrado'
        
    return Response(resultado,mimetype='application/json')
    
@app.route('/api/eliminarArticulo/<id>', methods = ['DELETE'])
def apiEliminarArticulo(id):
    respuesta = productos.delete_one({'_id':ObjectId(id)})
    if respuesta.deleted_count >=1:
        return 'Producto eliminado correctamente'
    else:
        return 'Producto no encontrado'
    
    
def verificarexistenciaProducto(codigo):    
    try:
        consulta = {"codigo":codigo}    
        producto = productos.find_one(consulta)
        return producto is not None       
    except pymongo.errors as error:
        print(error)
        return False