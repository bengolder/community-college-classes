import sqlite3
from dataclasses import dataclass

from utils import rjust, ljust


@dataclass
class ClassSchedule:
    campus: str
    path: str
    start_page: int
    end_page: int


@dataclass
class Line:
    page: int
    col: int
    font: str
    text: str
    index: int = -1

    def row(self):
        return [
            self.page,
            self.col,
            self.index,
            self.font,
            self.text,
        ]


# @dataclass
# class Discipline:
#     name: str
#     code: str
#     courses: list


# @dataclass
# class Course:
#     discipline: Discipline
#     title: str
#     number: str
#     units: str
#     summary: str
#     transferable_uc: bool
#     transferable_csu: bool


# @dataclass
# class Section:
#     course: Course
#     number: str
#     notes: str


# @dataclass
# class Meeting:
#     section: Section
#     type: str  # Lec/Lab
#     time: str
#     days: str
#     instructor: str
#     room: str
#     campus: str
