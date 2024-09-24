from app import app, items_collection
from flask import request, jsonify, redirect, render_template, session
import pymongo
import os
import pymongo.errors
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import json

@app.route("/productos")
def mostrar_productos():
    if "usuario" in session:
        try:
            mensaje = ""
            productos_lista = items_collection.find()
        except pymongo.errors as error:
            mensaje = str(error)

        return render_template("listarProductos.html", productos=productos_lista, mensaje=mensaje)
    else:
        mensaje = "Por favor, ingrese con sus credenciales"
        return render_template("frmLogin.html", mensaje=mensaje)

@app.route("/nuevo_producto", methods=['POST', 'GET'])
def nuevo_producto():
    if "usuario" in session:
        if request.method == 'POST':
            try:
                item = None
                codigo_item = int(request.form['txtCodigo'])
                nombre_item = request.form['txtNombre']
                precio_item = int(request.form['txtPrecio'])
                categoria_item = request.form['cbCategoria']
                imagen = request.files['fileFoto']
                nombre_imagen = secure_filename(imagen.filename)
                nombre_sin_extension = nombre_imagen.rsplit(".", 1)
                extension_imagen = nombre_sin_extension[1].lower()
                nombre_archivo_imagen = f"{codigo_item}.{extension_imagen}"
                
                item = {
                    "codigo": codigo_item, "nombre": nombre_item, "precio": precio_item,
                    "categoria": categoria_item, "foto": nombre_archivo_imagen
                }

                if not producto_existe(codigo_item):
                    resultado = items_collection.insert_one(item)
                    if resultado.acknowledged:
                        mensaje = "Producto agregado con éxito"
                        imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo_imagen))
                        return redirect('/productos')
                    else:
                        mensaje = "Error al agregar el producto."
                else:
                    mensaje = "Ya existe un producto con ese código"
            except pymongo.errors.PyMongoError as error:
                mensaje = error
            return render_template("frmAgregarProducto.html", mensaje=mensaje, producto=item)
        else:
            if request.method == 'GET':
                item = None
                return render_template("frmAgregarProducto.html", producto=item)
    else:
        mensaje = "Por favor, ingrese con sus credenciales"
        return render_template("frmLogin.html", mensaje=mensaje)

@app.route("/producto/<string:id>", methods=["GET"])
def ver_producto(id):
    if "usuario" in session:
        if request.method == 'GET':
            try:
                producto_id = ObjectId(id)
                consulta = {"_id": producto_id}
                item = items_collection.find_one(consulta)
                return render_template("frmActualizarProducto.html", producto=item)
            except pymongo.errors as error:
                mensaje = error
                return redirect("/productos")
    else:
        mensaje = "Por favor, ingrese con sus credenciales"
        return render_template("frmLogin.html", mensaje=mensaje)

def producto_existe(codigo):
    try:
        consulta = {"codigo": codigo}
        item = items_collection.find_one(consulta)
        return item is not None
    except pymongo.errors as error:
        print(error)
        return False

@app.route("/actualizar_producto", methods=["POST"])
def actualizar_item():
    if "usuario" in session:
        try:
            if request.method == "POST":
                codigo_item = int(request.form["txtCodigo"])
                nombre_item = request.form["txtNombre"]
                precio_item = int(request.form["txtPrecio"])
                categoria_item = request.form["cbCategoria"]
                producto_id = ObjectId(request.form["id"])
                imagen = request.files["fileFoto"]
                
                if imagen.filename != "":
                    nombre_imagen = secure_filename(imagen.filename)
                    nombre_sin_extension = nombre_imagen.rsplit(".", 1)
                    extension_imagen = nombre_sin_extension[1].lower()
                    nombre_archivo_imagen = f"{codigo_item}.{extension_imagen}"
                    
                    item = {
                        "_id": producto_id, "codigo": codigo_item, "nombre": nombre_item,
                        "precio": precio_item, "categoria": categoria_item, "foto": nombre_archivo_imagen
                    }
                else:
                    item = {
                        "_id": producto_id, "codigo": codigo_item, "nombre": nombre_item,
                        "precio": precio_item, "categoria": categoria_item
                    }
                    
                criterio = {"_id": producto_id}
                actualizacion = {"$set": item}
                existe = items_collection.find_one({"codigo": codigo_item, "_id": {"$ne": producto_id}})
                
                if existe:
                    mensaje = "Ya existe un producto con ese código"
                    return render_template("frmActualizarProducto.html", producto=item, mensaje=mensaje)
                else:
                    resultado = items_collection.update_one(criterio, actualizacion)
                    if resultado.acknowledged:
                        mensaje = "Producto actualizado"
                        if imagen.filename != "":
                            imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo_imagen))
                        return redirect("/productos")
        except pymongo.errors as error:
            mensaje = error
            return redirect("/productos")
    else:
        mensaje = "Por favor, ingrese con sus credenciales"
        return render_template("frmLogin.html", mensaje=mensaje)

@app.route("/eliminar_producto/<string:id>")
def eliminar_item(id):
    if "usuario" in session:
        try:
            producto_id = ObjectId(id)
            criterio = {"_id": producto_id}
            item = items_collection.find_one(criterio)
            print(item)
            nombre_archivo_imagen = item['foto']
            resultado = items_collection.delete_one(criterio)
            if resultado.acknowledged:
                mensaje = "Producto eliminado"
                if nombre_archivo_imagen != "":
                    ruta_imagen = app.config['UPLOAD_FOLDER'] + "/" + nombre_archivo_imagen
                    if os.path.exists(ruta_imagen):
                        os.remove(ruta_imagen)
        except pymongo.errors as error:
            mensaje = str(error)
        return redirect("/productos")
    else:
        mensaje = "Por favor, ingrese con sus credenciales"
        return render_template("frmLogin.html", mensaje=mensaje)

@app.route("/api/productos", methods=["GET"])
def api_productos():
    productos_lista = items_collection.find()
    lista = []
    for item in productos_lista:
        producto = {
            "_id": str(item['_id']),
            "codigo": item['codigo'],
            "nombre": item['nombre'],
            "precio": item['precio'],
            "categoria": item['categoria'],
            "foto": item['foto']
        }
        lista.append(producto)
    retorno = {'productos': lista}
    return jsonify(retorno)

@app.route("/api/producto/<string:id>", methods=["GET"])
def api_ver_producto(id):
    consulta = {"_id": ObjectId(id)}
    item = items_collection.find_one(consulta)
    producto = {
        "_id": str(item['_id']),
        "codigo": item['codigo'],
        "nombre": item['nombre'],
        "precio": item['precio'],
        "categoria": item['categoria'],
        "foto": item['foto']
    }
    retorno = {'producto': producto}
    return jsonify(retorno)

@app.route("/api/nuevo_producto", methods=["POST"])
def api_nuevo_producto():
    try:
        item = None
        mensaje = ""
        codigo_item = int(request.json['codigo'])
        nombre_item = request.json['nombre']
        precio_item = int(request.json['precio'])
        categoria_item = request.json['categoria']
        foto_item = request.json['foto']
        
        item = {
            "codigo": codigo_item, "nombre": nombre_item, "precio": precio_item,
            "categoria": categoria_item, "foto": foto_item
        }
        
        if not producto_existe(codigo_item):
            resultado = items_collection.insert_one(item)
            if resultado.acknowledged:
                mensaje = "Producto agregado correctamente"
            else:
                mensaje = "Error al agregar el producto."
        else:
            mensaje = f"Ya existe un producto con el código {codigo_item}"
    except pymongo.errors as error:
        mensaje = str(error)

    retorno = {"mensaje": mensaje}
    return jsonify(retorno)
