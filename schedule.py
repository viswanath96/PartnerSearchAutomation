# schedule.py

class Schedule:
    def __init__(self, day, date, count):
        self.day = day
        self.date = date
        self.count = count

    def display(self):
        return {
            "day": self.day,
            "date": self.date,
            "count": self.count
        }