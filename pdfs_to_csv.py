import csv
from dataclasses import dataclass

from pypdf import PdfReader


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


schedules = [
    ClassSchedule(
        "Berkeley City College",
        "data/pdfs/BCC Spring 24 Schedule V2.pdf",
        49,
        88,
    ),
    ClassSchedule(
        "Laney College",
        "data/pdfs/Laney Spring 24 Schedule V2.pdf",
        52,
        133,
    ),
    ClassSchedule(
        "College of Alameda",
        "data/pdfs/COA Spring 24 Schedule V2.pdf",
        45,
        81,
    ),
    ClassSchedule(
        "Merritt College",
        "data/pdfs/Merritt Spring 24 Schedule V2.pdf",
        49,
        83,
    ),
]

COL_X_THRESHOLD = 300
CONTENT_Y_TOP = 743
CONTENT_Y_BOTTOM = 24


# mutable module variables for script
last_page = 0
col_1_buffer = []
col_2_buffer = []


def is_primary_content(y):
    return CONTENT_Y_BOTTOM < y < CONTENT_Y_TOP


def visitor_for_page(page):
    def visitor(text, um, tm, font_dict, font_size):
        global last_page
        x = tm[-2]
        y = tm[-1]
        if text.strip() and is_primary_content(y):
            if page != last_page:
                last_page = page
            font = font_dict["/BaseFont"][8:]
            column = 1 if x < COL_X_THRESHOLD else 2
            line = Line(page, column, font, text)
            if column == 1:
                col_1_buffer.append(line)
            elif column == 2:
                col_2_buffer.append(line)

    return visitor


def drain_buffer_to_csv(csv_writer, buffer, index):
    while buffer:
        index += 1
        line = buffer.pop(0)
        line.index = index
        csv_writer.writerow(line.row())
    return index


if __name__ == "__main__":
    for schedule in schedules:
        slug = "-".join([schedule.campus, "2024", "Spring"]).lower().replace(" ", "_")
        reader = PdfReader(schedule.path)
        with open(f"data/csvs/{slug}.csv", "w", encoding="utf-8") as f:
            csv_writer = csv.writer(f, delimiter="\t")
            csv_writer.writerow(["page", "col", "index", "font", "text"])
            for page_index in range(schedule.start_page - 1, schedule.end_page):
                page = page_index + 1
                reader.pages[page_index].extract_text(
                    visitor_text=visitor_for_page(page)
                )
                line_index = 0
                line_index = drain_buffer_to_csv(csv_writer, col_1_buffer, line_index)
                drain_buffer_to_csv(csv_writer, col_2_buffer, line_index)
