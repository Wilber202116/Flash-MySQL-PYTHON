from flask import Blueprint, request, jsonify
from models.movieModel import create_movie, delete_movie, get_Movie_By_ID,get_Movies_By_Filter, listMovies, update_movie

movies_bp = Blueprint("movies", __name__)

# @movies_bp.route('/'),
# def noEsaqui(),:
    
#     return {"Hola": "pon movie en la url asi /movie/list"}

# Funcion para obtener todas las peliculas
# @movies_bp.route('/list'),
# def get_Movies(),:
#     movies = listMovies(),
#     if not movies:
#         return jsonify({'Message' : 'No hay peliculas'}),, 404
#     return jsonify(movies),

def validar_entero(valor):
    if valor == '' or valor is None:
        return ""
    try:
        return int(valor)
    except (ValueError, TypeError):
        return None

def validar_float(valor):
    if valor == '' or valor is None:
        return ""
    try:
        return float(valor)
    except (ValueError, TypeError):
        return None

@movies_bp.route('/list/<int:id>', methods=["GET"])
def get_Movie(id):
    movie = get_Movie_By_ID(id)
    if not movie:
        return jsonify({'Message' : 'No encontrado'}), 404
    
    return jsonify(movie)

@movies_bp.route('/list', methods=["GET"])
def get_Movies_By_Filtering():
    genero = request.args.get("genero")
    year_From = validar_entero(request.args.get("year_from"))
    year_To = validar_entero(request.args.get("year_to"))
    min_Rating = validar_float(request.args.get("calificacion"))
    order_BY = request.args.get("order_by")
    desC = request.args.get("desc")
    movies = get_Movies_By_Filter( genre=genero, year_from=year_From, year_to=year_To, min_rating=min_Rating, order_by=order_BY, desc=desC)
    if not movies:
        return jsonify({'Message' : 'No encontrado'}), 404
    if year_From is None or year_To is None:
        return jsonify({"Message": "el año debe ser un numero valido"})
    return jsonify(movies)

@movies_bp.route("/", methods=["POST"])
def add_movie():
    #recibimos los datos como json

    data = request.json

    titulo = data.get("titulo")
    director = data.get("director")
    anio = validar_entero(data.get("anio"))
    calificacion = validar_float(data.get("calificacion"))
    genero = data.get("genero")
    imagen = data.get("imagen")

    if anio is None:
        return jsonify({
            "message" : "El año debe ser un numero entero valido"
        }), 400

    if not titulo or not director:
        return jsonify({
            "message" : "Titulo, director y anio son obligatorios"
        }), 400
    if calificacion is None:
        return jsonify({
            "message" : "Calificacion debe ser numero valido"
        }), 400
    new_id = create_movie(titulo, director, anio, calificacion, genero, imagen)
    return jsonify({
        "message" : "pelicula registrada",
        "id" : new_id
    }), 201

@movies_bp.route("/<int:id>", methods=["PUT"])
def edit_movie(id):
    
    movie = get_Movie_By_ID(id)
    if not movie:
        return jsonify({"message": "Pelicula no encontrada"}), 400
    
    data = request.json

    titulo = data.get("titulo")
    director = data.get("director")
    anio = validar_entero(data.get("anio"))
    calificacion = validar_float(data.get("calificacion"))
    genero = data.get("genero")
    imagen = data.get("imagen")
    
    if anio is None:
        return jsonify({
            "message" : "El año debe ser un numero entero valido"
        }), 400

    if calificacion is None:
        return jsonify({
            "message" : "Calificacion debe ser numero valido"
        }), 400

    #print(type(titulo), type(director), type(anio), type(calificacion), type(genero),type(id))

    update = update_movie(titulo, director, anio, calificacion, genero, imagen, id)
    if update:
        return jsonify({
            "message" : "Pelicula actualizada"
        }), 201
    else:
        return jsonify({"Error" : "Faltan valores"}), 400

@movies_bp.route("/<int:id>", methods=["DELETE"])
def remove_movie(id):
    movie = get_Movie_By_ID(id)
    if not movie:
        return jsonify({
            "message": "Pelicula no encontrada"
        }), 404
    if delete_movie(id):
        return jsonify({
            "message" : "Pelicula eliminada"
        }), 200
    else:
        return jsonify({
            "Error": "Error al eliminar la pelicula"
        }), 400