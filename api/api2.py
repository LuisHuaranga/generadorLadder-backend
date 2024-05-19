from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos de ejemplo (en memoria)
productos = [
    {"id": 1, "nombre": "Producto 1", "precio": 10.0},
    {"id": 2, "nombre": "Producto 2", "precio": 20.0}
]

# Ruta para obtener todos los productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(productos)

# Ruta para obtener un producto por su ID
@app.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = next((p for p in productos if p["id"] == id), None)
    if producto:
        return jsonify(producto)
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 404

# Ruta para crear un nuevo producto
@app.route('/productos', methods=['POST'])
def crear_producto():
    nuevo_producto = request.json
    nuevo_producto["id"] = len(productos) + 1
    productos.append(nuevo_producto)
    return jsonify({"mensaje": "Producto creado", "id": nuevo_producto["id"]}), 201

# Ruta para actualizar un producto por su ID
@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    producto = next((p for p in productos if p["id"] == id), None)
    if producto:
        datos_actualizados = request.json
        producto.update(datos_actualizados)
        return jsonify({"mensaje": "Producto actualizado"}), 200
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 404

# Ruta para eliminar un producto por su ID
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    global productos
    productos = [p for p in productos if p["id"] != id]
    return jsonify({"mensaje": "Producto eliminado"}), 200

if __name__ == '__main__':
    app.run(debug=True,port=8080)
