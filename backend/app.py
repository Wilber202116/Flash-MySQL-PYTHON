from flask import Flask, request
from flask_cors import CORS
from routes.movies import movies_bp
from database import get_db

#instancia de flask
app = Flask(__name__)
CORS(app)

app.register_blueprint(movies_bp, url_prefix='/movies')

@app.route('/')
def conection():
    try:
        conn = get_db()
        cursor = conn.cursor()
        # Comando de prueba
        cursor.execute("SELECT NOW()")
        result = cursor.fetchone() # cuando recibimos una sola fila
        return { "time": str(result[0]) }
    except Exception as e:
        return { "Error" : str(e) }

#punto de partida
if __name__ == '__main__':
    app.run(debug=True)