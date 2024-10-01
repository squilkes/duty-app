class Postman:
    def __init__(self, name):
        self.name = name
        self.known_routes = []

    def add_route(self, route):
        if route not in self.known_routes:
            self.known_routes.append(route)
