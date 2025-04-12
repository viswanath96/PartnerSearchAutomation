# schedule.py

class Schedule:
    def __init__(self, day, date, occurance):
        self.day = day
        self.date = date
        self.occurance = occurance

    def display(self):
        return {
            "day": self.day,
            "date": self.date,
            "occurance": self.occurance
        }