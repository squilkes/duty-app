import sqlite3

def init_db():
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS Postmen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS Routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS Postman_Route (
            postman_id INTEGER,
            route_id INTEGER,
            FOREIGN KEY(postman_id) REFERENCES Postmen(id),
            FOREIGN KEY(route_id) REFERENCES Routes(id),
            PRIMARY KEY (postman_id, route_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_postman(name):
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO Postmen (name) VALUES (?)", (name,))
    postman_id = c.lastrowid
    conn.commit()
    conn.close()
    return postman_id

def get_all_postmen():
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Postmen")
    postmen = c.fetchall()
    conn.close()
    return postmen

def get_postman_routes(postman_id):
    """Get all routes that a postman knows."""
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("SELECT route_id FROM Postman_Route WHERE postman_id = ?", (postman_id,))
    routes = [row[0] for row in c.fetchall()]  # Return only route_ids
    conn.close()
    return routes


def assign_route_to_postman(postman_id, route_id):
    """Assign a route to a postman."""
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO Postman_Route (postman_id, route_id) VALUES (?, ?)", (postman_id, route_id))
    conn.commit()
    conn.close()


def clear_postman_routes(postman_id):
    """Remove all routes associated with a postman."""
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("DELETE FROM Postman_Route WHERE postman_id = ?", (postman_id,))
    conn.commit()
    conn.close()


def update_postman_name(postman_id, new_name):
    """Update a postman's name."""
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("UPDATE Postmen SET name = ? WHERE id = ?", (new_name, postman_id))
    conn.commit()
    conn.close()


def delete_postman(postman_id):
    """Delete a postman and remove associated routes."""
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()

    # First, remove any route associations with this postman
    c.execute("DELETE FROM Postman_Route WHERE postman_id = ?", (postman_id,))

    # Then, remove the postman from the Postmen table
    c.execute("DELETE FROM Postmen WHERE id = ?", (postman_id,))

    conn.commit()
    conn.close()

def add_route(name):
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO Routes (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_all_routes():
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Routes")
    routes = c.fetchall()
    conn.close()
    return routes

def update_route_name(route_id, new_name):
    """Update a route's name."""
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()
    c.execute("UPDATE Routes SET name = ? WHERE id = ?", (new_name, route_id))
    conn.commit()
    conn.close()

def delete_route(route_id):
    """Delete a route from the Routes table."""
    conn = sqlite3.connect('duty_app.db')
    c = conn.cursor()

    # First, remove any associations with this route in the Postman_Route table
    c.execute("DELETE FROM Postman_Route WHERE route_id = ?", (route_id,))

    # Then, remove the route from the Routes table
    c.execute("DELETE FROM Routes WHERE id = ?", (route_id,))

    conn.commit()
    conn.close()