import re

from pypdf import PdfReader
from collections import namedtuple

ClassSchedule = namedtuple("ClassSchedule", "campus path start_page end_page")

schedules = [
    # ClassSchedule(
    #     "Berkeley City College",
    #     "pdfs/BCC Spring 24 Schedule V2.pdf",
    #     49,
    #     88,
    # ),
    # ClassSchedule(
    #     "Laney College",
    #     "pdfs/Laney Spring 24 Schedule V2.pdf",
    #     52,
    #     133,
    # ),
    # ClassSchedule(
    #     "College of Alameda",
    #     "pdfs/COA Spring 24 Schedule V2.pdf",
    #     45,
    #     81,
    # ),
    ClassSchedule(
        "Merritt College",
        "pdfs/Merritt Spring 24 Schedule V2.pdf",
        49,
        83,
    ),
]


def nice_int(n, width=3):
    return str(int(n)).rjust(width, " ")


last_page = 0
last_column = 0
COL_X_THRESHOLD = 300
CONTENT_Y_TOP = 743
CONTENT_Y_BOTTOM = 24


def is_primary_content(y):
    return CONTENT_Y_BOTTOM < y < CONTENT_Y_TOP


def visitor_for_page(page):
    def visitor(text, um, tm, font_dict, font_size):
        global last_page
        global last_column
        x = tm[-2]
        y = tm[-1]
        if text.strip() and is_primary_content(y):
            font = font_dict["/BaseFont"][8:]
            column = 1 if x < COL_X_THRESHOLD else 2
            if column != last_column:
                print(f"Switching to column {column}")
                last_column = column
            print(
                f"P: {page + 1}",
                nice_int(x),
                nice_int(y),
                [text],
                font,
            )
            return text

    return visitor


for schedule in schedules:
    slug = "-".join([schedule.campus, "2024", "Spring"]).lower().replace(" ", "_")
    reader = PdfReader(schedule.path)
    with open(f"txts/{slug}.txt", "w", encoding="utf-8") as f:
        # for i in range(schedule.start_page - 1, schedule.end_page):
        for i in range(schedule.start_page - 1, schedule.start_page + 2):
            f.write(f"\n\n$ PAGE {i + 1}\n\n")
            f.write(reader.pages[i].extract_text(visitor_text=visitor_for_page(i)))
