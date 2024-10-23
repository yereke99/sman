from sqlite3 import connect
from xlsxwriter.workbook import Workbook
import random
from datetime import datetime

class Database():
    def __init__(self) -> None:
        self.db = connect('sman.db')
        self.cursor = self.db.cursor()


if __name__ == "__main__":
    db = Database()