from flask import Flask, render_template
import os

app = Flask(__name__, static_folder='Web/static', template_folder='Web')

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/usuarios')
def serve_usuarios():
    return render_template('usuarios.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6060)
