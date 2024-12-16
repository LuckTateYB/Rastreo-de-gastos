from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'


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

# Modelo Usuarios

class Usuario(db.Model):
    __tablename__ = "Usuarios"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gastos = db.relationship('Gasto', backref='usuario', lazy=True)



# Modelo para los gastos
class Gasto(db.Model):
    __tablename__ = 'gastos'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)

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

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return redirect(url_for('welcome'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Usuario.query.filter_by(username=username).first():
            return jsonify({'error': 'El nombre de usuario ya existe'}), 400
        hashed_password = generate_password_hash(password)
        nuevo_usuario = Usuario(username=username, password=hashed_password)
        
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    usuario = Usuario.query.filter_by(username=username).first()
    if usuario and check_password_hash(usuario.password, password):
        session['user_id'] = usuario.id
        return redirect(url_for('index'))
    return jsonify({'error': 'Credenciales incorrectas'}), 401

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/agregar_gasto", methods=["POST"])
def agregar_gasto():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    user_id = session['user_id']
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
        fecha=fecha,
        user_id=user_id
        )
        db.session.add(nuevo_gasto)
        db.session.commit()
        return jsonify({'message': 'Gasto agregado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route("/listar_gastos", methods=["GET"])
def listar_gastos():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 401

    user_id = session['user_id']
    gastos = Gasto.query.filter_by(user_id=user_id).all()
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
    

