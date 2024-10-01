import sqlite3

def init_db():
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Postmen (id INTEGER PRIMARY KEY, name TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS Routes (id INTEGER PRIMARY KEY, name TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS Postman_Route (postman_id INTEGER, route_id INTEGER, PRIMARY KEY (postman_id, route_id))')
    conn.commit()
    conn.close()

def add_postman(name):
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO Postmen (name) VALUES (?)", (name,))
    postman_id = c.lastrowid  # Retrieve the generated postman_id
    conn.commit()
    conn.close()
    return postman_id  # Return the ID of the newly added postman

def add_route(name):
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO Routes (name) VALUES (?)", (name,))
    route_id = c.lastrowid  # Retrieve the generated route_id
    conn.commit()
    conn.close()
    return route_id  # Return the ID of the newly added route

def get_all_routes():
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Routes")
    routes = c.fetchall()
    conn.close()
    return routes

def get_all_postmen():
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Postmen")
    postmen = c.fetchall()
    conn.close()
    return postmen

def get_postman_routes(postman_id):
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("SELECT route_id FROM Postman_Route WHERE postman_id = ?", (postman_id,))
    routes = [row[0] for row in c.fetchall()]
    conn.close()
    return routes

def assign_route_to_postman(postman_id, route_id):
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO Postman_Route (postman_id, route_id) VALUES (?, ?)", (postman_id, route_id))
    conn.commit()
    conn.close()

def clear_postman_routes(postman_id):
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("DELETE FROM Postman_Route WHERE postman_id = ?", (postman_id,))
    conn.commit()
    conn.close()

def update_postman_name(postman_id, new_name):
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("UPDATE Postmen SET name = ? WHERE id = ?", (new_name, postman_id))
    conn.commit()
    conn.close()

def delete_postman(postman_id):
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("DELETE FROM Postman_Route WHERE postman_id = ?", (postman_id,))
    c.execute("DELETE FROM Postmen WHERE id = ?", (postman_id,))
    conn.commit()
    conn.close()

def update_route_name(route_id, new_name):
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("UPDATE Routes SET name = ? WHERE id = ?", (new_name, route_id))
    conn.commit()
    conn.close()

def delete_route(route_id):
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("DELETE FROM Postman_Route WHERE route_id = ?", (route_id,))
    c.execute("DELETE FROM Routes WHERE id = ?", (route_id,))
    conn.commit()
    conn.close()

def postman_knows_route(postman_id, route_id):
    """Check if a postman knows a particular route."""
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    query = """
    SELECT 1 FROM Postman_Route
    WHERE postman_id = ? AND route_id = ?
    """
    c.execute(query, (postman_id, route_id))
    result = c.fetchone()
    conn.close()
    return result is not None
