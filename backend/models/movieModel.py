from database import get_db
import mysql.connector 

# Obtener una sola peliculas por ID
def get_Movie_By_ID(id):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM peliculas WHERE id = {id} ", ())

        row = cursor.fetchone()
        return row
    except mysql.connector.Error as e:
        print("Error al obtener pelicula", {e})
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def listMovies():

    conn = None
    cursor = None
    try:
        # conectamos con la base de datos
        conn = get_db()
        # pedimos a las tablas en forma de diccionario
        cursor = conn.cursor(dictionary=True)
        # crear cosulta a la base de datos
        query = "SELECT * FROM peliculas"
        # ejercutar consulta 
        cursor.execute(query)
        # recibir las tablas
        rows = cursor.fetchall() # Obtiene todas la peliculas
        # fetchall es para obtener todas las filas
        # retornar la informacion
        return rows
    except mysql.connector.Error as err:
        print("Error al traer las peliculas: ", err)
        return []
    finally: 
        if cursor: cursor.close()
        if conn : conn.close()

# Obtener peliculas con filtros personalizados
def get_Movies_By_Filter(genre = None, year_from=None, year_to=None, min_rating=None, order_by=None, desc=None): 
    conn = None
    cursor = None
    try:
        conn = get_db()
        query = "SELECT * FROM peliculas"
        cursor = conn.cursor(dictionary=True)
        params = [] # filtros
        parts = []

        if genre:
            parts.append("genero = %s")
            params.append(genre)
        if year_from:
            parts.append("anio >= %s")
            params.append(year_from)
        if year_to:
            parts.append("anio <= %s")
            params.append(year_to)
        if min_rating:
            parts.append("calificacion >= %s")
            params.append(min_rating)
        
        # Si vienen filtros
        if parts:
            query += " WHERE " + " AND ".join(parts)
        
        if order_by in ["titulo", "anio", "calificacion", "genero", "director"]:
            if bool(desc) == True:
                query += f"ORDER BY {order_by} DESC"
            else:
                query += f"ORDER BY {order_by}"
        
        #print(query),
        #print(parts),
        #print(params),
        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print("Error con los filtros: ", err)
    finally: 
        if cursor: cursor.close()
        if conn : conn.close()

def create_movie(titulo, director, anio, calificacion, genero, imagen):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO peliculas (titulo, director, anio, calificacion, genero, imagen)
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (titulo, director, anio, calificacion, genero, imagen)
        )
        conn.commit()
        last_id = cursor.lastrowid # Devuelve el ultimo ID
        return last_id
    except mysql.connector.Error as err:
        print("Error al creal la pelicula ", err)
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_movie(titulo, director, anio, calificacion, genero, imagen,id):
    conn = None
    cursor = None
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE peliculas 
            SET titulo=%s, director=%s, anio=%s, calificacion=%s, genero=%s, imagen=%s
            WHERE id=%s
            """,
            (titulo, director, anio, calificacion, genero, imagen, id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print("Error al actualizar: ", err)
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_movie(id):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM peliculas WHERE id = {id}", ())# la coma en id es necesario, esto es una dupla
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print("Error al eliminar: ", err)
        return False
    finally:
        if cursor: cursor.close()

        if conn: conn.close()
