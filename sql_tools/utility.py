from datetime import datetime as dt

class Utility():
    def __init__(self):
        self.aa = 0
    def convert_datetime_to_str(self, date_t):
        return date_t.strftime('%Y-%m-%d')
