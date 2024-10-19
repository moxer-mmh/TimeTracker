from datetime import datetime


class TimeEntry:
    def __init__(
        self,
        date,
        arrival_time=None,
        lunch_start=None,
        lunch_end=None,
        departure_time=None,
        balance=0,
    ):
        self.date = date
        self.arrival_time = arrival_time
        self.lunch_start = lunch_start
        self.lunch_end = lunch_end
        self.departure_time = departure_time
        self.balance = balance

    @staticmethod
    def calculate_balance(arrival, lunch_start, lunch_end, departure):
        def time_to_minutes(time_str):
            hours, minutes = map(int, time_str.split(":"))
            return hours * 60 + minutes

        work_time = (time_to_minutes(lunch_start) - time_to_minutes(arrival)) + (
            time_to_minutes(departure) - time_to_minutes(lunch_end)
        )
        return work_time - 450

    def is_complete(self):
        return all(
            [self.arrival_time, self.lunch_start, self.lunch_end, self.departure_time]
        )

    def update_balance(self):
        if self.is_complete():
            self.balance = self.calculate_balance(
                self.arrival_time, self.lunch_start, self.lunch_end, self.departure_time
            )
