from bottle import get, post, run, request, respons
import sqlite3

db = sqlite3.connect("")

def hash(msg):
    import hashlib
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

@get('/ping')
def get_ping():
    response.status = 200
    return "pong"

@post('/reset')
def post_reset():
    c = db.cursor()
    c.execute(
        """
        """
    )
    found = [{}]
    response.status = 200
    return {"data": found}

@post('/users')
def post_users():
    # TODO
    c = db.cursor()
    c.execute(
        """
        """
    )
    found = [{}]
    response.status = 200
    return {"data": found}

@post('/movies')
def post_movies():
    movie = request.json
    c = db.cursor()
    c.execute(
        """
        """
    )
    found = [{}]
    response.status = 200
    return {"data": found}

@get('/movies')
def get_movies():
    query = """
        """
    params = []
    if request.query.title:
        query += ""
        params.append(unquote(request.query.title))
    c = db.cursor()
    c.execute(query, params)
    found = [{}]
    response.status = 200
    return {"data": found}

@post('/performances')
def post_performances():
    performance = request.json
    c = db.cursor()
    c.execute(
        """
        """
    )
    found = [{}]
    if not found:
        response.status = 400
        return "Illegal..."
    else:
        db.commit()
        response.status = 201
        _ = found
        return f""

run(host='localhost', port=8080)