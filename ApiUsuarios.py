from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://practicas:A644DDA27009E1@31.220.101.168:3306/practicas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    ID = db.Column(db.Integer, primary_key=True)
    IDRol = db.Column(db.Integer, nullable=False)
    Contrasena = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    FechaRegistro = db.Column(db.Date, nullable=False)
    Nombre = db.Column(db.String(100), nullable=False)

def obtener_rol(rol):
    if rol == 1:
        return 'Administrador'
    elif rol == 2:
        return 'Usuario'
    return 'Desconocido'

@app.route('/api/filtrar', methods=['POST'])
def filtrar_usuario():
    try:
        email = request.json.get('email')
        usuario = Usuario.query.filter_by(Email=email).first()

        if usuario:
            return jsonify({
                'nombre': usuario.Nombre,
                'email': usuario.Email,
                'rol': obtener_rol(usuario.IDRol),
                'password': usuario.Contrasena
            }), 200
        return jsonify({"message": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"message": f"Error del servidor: {str(e)}"}), 500

@app.route('/api/modificar', methods=['POST'])
def modificar_usuario():
    try:
        data = request.json
        email = data.get('email')
        nombre = data.get('nombre')
        rol = data.get('rol')
        password = data.get('password')

        if rol.lower() == 'administrador':
            rol = 1
        elif rol.lower() == 'usuario':
            rol = 2

        usuario = Usuario.query.filter_by(Email=email).first()

        if usuario:
            usuario.Nombre = nombre
            usuario.IDRol = rol
            usuario.Contrasena = password

            db.session.commit()

            return jsonify({"message": "Datos del usuario actualizados correctamente"}), 200

        return jsonify({"message": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"message": f"Error del servidor: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9091)
