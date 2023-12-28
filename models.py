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

    def __repr__(self):
        return " ".join(
            [
                rjust(f"p{self.page}", width=4),
                rjust(f"c{self.col}", width=2),
                rjust(f"i{self.index}", width=4),
                ljust(self.font, width=23),
                str([self.text]),
            ]
        )


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
