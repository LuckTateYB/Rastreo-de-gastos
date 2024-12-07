from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

gastos = []

@app.route('/')
def index():
    # return "Hola Mundo!"
    return render_template('index.html')

@app.route("/agregar_gasto", methods=["POST"])
def agregar_gasto():
    data = request.get_json()
    descripcion = data.get("descripcion")
    monto = data.get("monto")
    categoria = data.get("categoria")
    fecha = data.get("fecha")
    
    # Validar los datos
    if not descripcion or not monto or not categoria or not fecha:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    
    # Agregar el gasto a la lista
    gasto = {
        "descripcion": descripcion,
        "monto": float(monto),
        "categoria": categoria,
        "fecha": fecha
    }
    gastos.append(gasto)
    return jsonify({"message": "Gasto agregado correctamente", "gastos": gastos}), 200

@app.route("/listar_gastos", methods=["GET"])
def listar_gastos():
    return jsonify(gastos)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

