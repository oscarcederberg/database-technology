import sqlite3

from urllib.parse import quote, unquote
from bottle import get, post, run, request, response

HOST = "127.0.0.1"
PORT = 8888
RESET_SCRIPT = """
DELETE FROM cookies;
DELETE FROM ingredients;
DELETE FROM recipe_lines;
DELETE FROM customers;
DELETE FROM orders;
DELETE FROM order_rows;
DELETE FROM pallets;
"""

db = sqlite3.connect("krusty-db.sqlite")

#   POST empty
#   location (205)
@post('/reset')
def post_reset():
    c = db.cursor()
    c.executescript(RESET_SCRIPT)
    response.status = 205
    return { "location": "/" }

#   POST name, address
#   location (201)
@post('/customers')
def post_customers():
    customer = request.json
    c = db.cursor()
    c.execute(
        """
        INSERT
        INTO        customers(customer_name, address)
        VALUES      (?, ?)
        """,
        [customer['name'], customer['address']]
    )
    db.commit()
    response.status = 201
    return { 'location': f'/customers/' + quote(customer['name']) }

#   GET
#   data: [name, address] (200)
@get('/customers')
def get_customers():
    c = db.cursor()
    c.execute(
        """
        SELECT customer_name, address
        FROM customers
        """
    )
    found = [{'customer_name': name, 'address': address} for name, address in c]
    response.status = 200
    return { 'data': found }

#   POST ingredient, unit
#   location (201)
@post('/ingredients')
def post_ingredients():
    ingredient = request.json
    c = db.cursor()
    c.execute(
        """
        INSERT
        INTO        ingredients(ingredient_name, unit)
        VALUES      (?, ?)
        """,
        [ingredient['ingredient'], ingredient['unit']]
    )
    db.commit()
    response.status = 201
    return { 'location': f'/ingredients/' + quote(ingredient['ingredient']) }

#   POST deliveryTime, quantity
#   data: {ingredient, quantity, unit} (201)
@post('/ingredients/<ingredient_name>/deliveries')
def post_ingredient_deliveries(ingredient_name):
    delivery = request.json
    c = db.cursor()
    c.execute(
        """
        UPDATE      ingredients
        SET         delivery_datetime = ?,
                    delivery_amount = ?
        WHERE       ingredient_name = ?
        RETURNING   ingredient_name, total_amount, unit
        """,
        [delivery['deliveryTime'], delivery['quantity'], ingredient_name]
    )
    found = [{ 'ingredient': ingredient, 'quantity': quantity, 'unit': unit} for ingredient, quantity, unit in c ]
    response.status = 201
    return { 'data': found }

#   GET
#   data: [ingredient, quantity, unit] (200)
@get('/ingredients')
def get_ingredients():
    c = db.cursor()
    c.execute(
        """
        SELECT ingredient_name, total_amount, unit
        FROM ingredients
        """
    )
    found = [{'ingredient': ingredient, 'quantity': quantity, 'unit': unit} for ingredient, quantity, unit in c]
    response.status = 200
    return { 'data': found }

#   POST name, recipe: [ingredient, amount]
#   location (201)
@post('/cookies')
def post_cookies():
    cookie = request.json
    c = db.cursor()
    for i in cookie['recipe']:
        c.execute(
        """
        INSERT
        INTO        recipe_lines(product_name, ingredient_name, amount)
        VALUES      (?, ?, ?)
        
        """,
        [cookie['name'], i['ingredient'], i['amount']]
        )
    db.commit()
    response.status = 201
    return { 'location': f'/cookies/' + quote(cookie['name']) }

#   GET
#   data: [name, pallets] (200)
@get('/cookies')
def get_cookies():
    c = db.cursor()
    c.execute(
        """
        WITH cookies_with_pallets AS (
            SELECT      product_name, count()
            FROM        cookies
            LEFT JOIN   pallets USING (product_name)
            WHERE       is_blocked = 0
            GROUP BY    product_name
        )
        SELECT      product_name, count() AS pallet_amount
        FROM        cookies
        LEFT JOIN   cookies_with_pallets USING (product_name)
        GROUP BY    product_name
        """
    )
    found = [{'name': name, 'pallets': pallets} for name, pallets in c]
    response.status = 200
    print(found)
    return { 'data': found }

#   GET
#   SUCCESS: data: [ingredient, amount, unit] (200)
#   FAILURE: data: [] (404)
@get('/cookies/<cookie_name>/recipe')
def get_cookie_recipe(cookie_name):
    c = db.cursor()
    c.execute(
        """
        SELECT ingredient, amount, unit
        FROM recipe_lines
        JOIN ingredients USING (ingredient_name)
        WHERE product_name = ?
        """,
        [unquote(cookie_name)]
    )
    found = [{'ingredient': ingredient, 'amount': amount, 'unit': unit} for ingredient, amount, unit in c]
    if not found:
        response.status = 404
    else:
        response.status = 200
    return { 'data': found }

#   POST cookie
#   SUCCESS: location (201)
#   FAILURE: location (422)
@post('/pallets')
def post_pallets():
    cookie = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO        pallets(product_name, production_datetime)
            VALUES      (?, datetime('now'))
            RETURNING   pallet_number
            """,
            [cookie['cookie']]
        )
        found = c.fetchone() 
        response.status = 201
        db.commit()
        return { 'location': f'/pallets/' + found[0]}
    except:
        response.status = 422
        return { 'location': ''}

#   GET ?cookie, ?after, ?before
#   data: [id, cookie, productionDate, blocked] (200)
@get('/pallets')
def get_pallets():
    query = """
        SELECT pallet_number, product_name, production_datetime, is_blocked
        FROM pallets
        WHERE 1 is 1
        """
    params = []
    if request.query.cookie:
        query += " AND product_name == ?"
        params.append(unquote(request.query.cookie))
    if request.query.after:
        query += " AND production_datetime > ?"
        params.append(unquote(request.query.after))
    if request.query.before:
        query += " AND production_datetime < ?"
        params.append(unquote(request.query.before))
    c = db.cursor()
    c.execute(query, params)
    found = [{'id': id, 'cookie': cookie, 'productionDate': productionDate, "blocked": blocked} for id, cookie, productionDate, blocked in c]
    response.status = 200
    return {'data': found}

#   POST ?before, ?after
#   "" (205)
@post('/cookies/<cookie_name>/block')
def post_cookie_block(cookie_name):
    query = """
        UPDATE pallets
        SET is_blocked = 1
        WHERE product_name = ?
        """
    params = [cookie_name]
    if request.query.after:
        query += " AND production_datetime > ?"
        params.append(unquote(request.query.after))
    if request.query.before:
        query += " AND production_datetime < ?"
        params.append(unquote(request.query.before))
    c = db.cursor()
    c.execute(query, params)
    response.status = 205
    return ""

#   POST ?before, ?after
#   "" (205)
@post('/cookies/<cookie_name>/unblock')
def post_cookie_unblock(cookie_name):
    query = """
        UPDATE pallets
        SET is_blocked = 0
        WHERE product_name = ?
        """
    params = [cookie_name]
    if request.query.after:
        query += " AND production_datetime > ?"
        params.append(unquote(request.query.after))
    if request.query.before:
        query += " AND production_datetime < ?"
        params.append(unquote(request.query.before))
    c = db.cursor()
    c.execute(query, params)
    response.status = 205
    return ""

run(host=HOST, port=PORT)