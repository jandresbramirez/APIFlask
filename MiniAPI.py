from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos simulados: películas y sus directores
movies = [
    {
        "id": 1,
        "title": "Inception",
        "director": "Christopher Nolan",
        "year": 2010
    },
    {
        "id": 2,
        "title": "Pulp Fiction",
        "director": "Quentin Tarantino",
        "year": 1994
    },
    {
        "id": 3,
        "title": "The Matrix",
        "director": "Lana y Lilly Wachowski",
        "year": 1999
    }
]

# Obtener todas las películas
@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies), 200

# Obtener una película por ID
@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if movie is None:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(movie), 200

# Crear una nueva película
@app.route('/movies', methods=['POST'])
def create_movie():
    if not request.json or 'title' not in request.json or 'director' not in request.json or 'year' not in request.json:
        return jsonify({'error': 'Bad request'}), 400
    
    new_id = max(m['id'] for m in movies) + 1 if movies else 1

    # Evitar duplicados por título y director
    if any(m['title'] == request.json['title'] and m['director'] == request.json['director'] for m in movies):
        return jsonify({'error': 'Movie already exists'}), 400
    
    movie = {
        "id": new_id,
        "title": request.json['title'],
        "director": request.json['director'],
        "year": request.json['year']
    }
    movies.append(movie)
    return jsonify(movie), 201

# Actualizar una película
@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if movie is None:
        return jsonify({'error': 'Movie not found'}), 404
    if not request.json:
        return jsonify({'error': 'Bad request'}), 400

    movie['title'] = request.json.get('title', movie['title'])
    movie['director'] = request.json.get('director', movie['director'])
    movie['year'] = request.json.get('year', movie['year'])
    
    return jsonify(movie), 200

# Eliminar una película
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if movie is None:
        return jsonify({'error': 'Movie not found'}), 404
    movies.remove(movie)
    return jsonify({'result': 'Movie deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
