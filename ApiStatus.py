import socket
import threading
import time
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

SERVICIOS = {
    'VPS': 22,
    'CNC': 1212,
    'Servidor Web': 7080,  
    'Bot Discord': 80,
}

estado_servicios = {}

MAX_INTENTOS = 3

def comprobar_estado_puerto(ip, puerto, servicio):
    fallos = 0  
    exitos = 0  

    for intento in range(MAX_INTENTOS):
        try:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)  
                resultado = s.connect_ex((ip, puerto))
                
                if resultado == 0:
                    exitos += 1
                    print(f"Prueba {intento + 1} al puerto {puerto} de {servicio} exitosa.")
                else:
                    fallos += 1
                    print(f"Prueba {intento + 1} al puerto {puerto} de {servicio} fallida.")
        except socket.error:
            fallos += 1
            print(f"Prueba {intento + 1} al puerto {puerto} de {servicio} fallida debido a un error de socket.")
        
        time.sleep(1.5)

    if fallos == MAX_INTENTOS:
        estado = "Inalcanzable" 
    elif fallos > 0:
        estado = "Intermitente"  
    else:
        estado = "Operando"  
    
    print(f"Estado final para el servicio {servicio}: {estado}")
    estado_servicios[servicio] = estado


def actualizar_estado_servicios():
    ip = '31.220.101.168'  
    while True:
        hilos = []
        
        for servicio, puerto in SERVICIOS.items():
            hilo = threading.Thread(target=comprobar_estado_puerto, args=(ip, puerto, servicio))
            hilos.append(hilo)
            hilo.start()
        
        for hilo in hilos:
            hilo.join()
        
        time.sleep(1)  


@app.route('/estado', methods=['GET'])
def obtener_estado():
    return jsonify(estado_servicios)


if __name__ == '__main__':
    hilo_actualizacion = threading.Thread(target=actualizar_estado_servicios, daemon=True)
    hilo_actualizacion.start()

    app.run(host='0.0.0.0', port=6061)
