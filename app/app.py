from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

DB_USER = 'sa'
DB_PASSWORD = 'oscar123456'
DB_SERVER = 'OSCARFABIAN'
DB_NAME = 'rastreo_gastos'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para los gastos
class Gasto(db.Model):
    __tablename__ = 'gastos'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'monto': self.monto,
            'categoria': self.categoria,
            'fecha': self.fecha.strftime('%Y-%m-%d')
        }

# Test de conection a la base de datos
def test_db_connection():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Conexión Exitosa:", [row[0] for row in result])
        return True
    except Exception as e:
        print(f"Error al conectarse: {str(e)}")
        return False

# Creando tabla por defecto
def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {str(e)}")

@app.route('/')
def index():
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
    
    try:
        # Crear una instancia de Gasto
        nuevo_gasto = Gasto(
            descripcion=descripcion,
            monto=monto,
            categoria=categoria,
            fecha=fecha
        )
        db.session.add(nuevo_gasto)
        db.session.commit()
        return jsonify({'message': 'Gasto agregado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route("/listar_gastos", methods=["GET"])
def listar_gastos():
    gastos = Gasto.query.all()
    lista_gastos = [
        {
            'descripcion': gasto.descripcion,
            'monto': gasto.monto,
            'categoria': gasto.categoria,
            'fecha': gasto.fecha.strftime('%Y-%m-%d')
        }
        for gasto in gastos
    ]
    return jsonify(lista_gastos)


if __name__ == '__main__':
    with app.app_context():
        if test_db_connection():
            init_db()
            app.run(debug=True, port=5000)
        else:
            print("Error: no se puede conectar a la base de datos. Verifique configuración.")
    

