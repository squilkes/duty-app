from random import choice

class ScheduleManager:
    def __init__(self, postmen, routes):
        self.postmen = postmen
        self.routes = routes
        self.schedule = {}

    def create_schedule(self, week_number):
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        # Assign each postman a rotating day off
        for postman in self.postmen:
            day_off = days_of_week[week_number % len(days_of_week)]
            print(f"{postman.name}'s day off is {day_off}")

        # Assign postmen to routes
        for day in days_of_week:
            self.schedule[day] = {}
            for route in self.routes:
                available_postmen = [p for p in self.postmen if day not in p.known_routes]
                if available_postmen:
                    assigned_postman = choice(available_postmen)
                    self.schedule[day][route.name] = assigned_postman.name

    def print_schedule(self):
        for day, assignments in self.schedule.items():
            print(f"{day}:")
            for route, postman in assignments.items():
                print(f"  {route} - {postman}")
