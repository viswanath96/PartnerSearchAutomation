# schedule.py

class Schedule:
    def __init__(self, day, date, occurance):
        self.day = day
        self.date = date
        self.occurance = occurance

    def to_dict(self):
        return {
            "day": self.day,
            "date": self.date,
            "count": self.count
        }

    def display(self):
        return self.to_dict()
