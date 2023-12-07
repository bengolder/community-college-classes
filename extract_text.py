from pypdf import PdfReader
from collections import namedtuple

ClassSchedule = namedtuple(
    "ClassSchedule", "campus filename year semester start_page end_page"
)

schedules = [
    ClassSchedule(
        "Berkeley City College",
        "Berkeley Summer Fall 2023 (V2.3).pdf",
        2023,
        "Fall",
        60,
        99,
    ),
    # ClassSchedule(
    #     "Laney College", "Laney Summer Fall 2023 (V2.3)1.pdf", 2023, "Fall", 70, 142
    # ),
    # ClassSchedule(
    #     "College of Alameda",
    #     "Alameda Summer Fall 2023 (V2.3).pdf",
    #     2023,
    #     "Fall",
    #     55,
    #     90,
    # ),
    # ClassSchedule(
    #     "Merritt College", "Merritt Summer Fall 2023 (V2.3).pdf", 2023, "Fall", 58, 91
    # ),
]
last_x = 0
last_y = 0


def nice_int(n, width=3):
    return str(int(n)).rjust(width, " ")


def visitor(text, um, tm, font_dict, font_size):
    global last_x
    global last_y
    if text.strip():
        x = tm[-2]
        y = tm[-1]
        dx = x - last_x
        dy = y - last_y
        last_x = x
        last_y = y
        d = abs(dx * dy)
        if d > 100000:  # and 10 < x < 100:
            print(
                nice_int(x),
                nice_int(y),
                nice_int(d, 4),
                nice_int(dx, 4),
                nice_int(dy, 4),
                [text],
            )


for schedule in schedules:
    slug = (
        "-".join([schedule.campus, str(schedule.year), schedule.semester])
        .lower()
        .replace(" ", "_")
    )
    reader = PdfReader(f"pdfs/{schedule.filename}")
    with open(f"txts/{slug}.txt", "w", encoding="utf-8") as f:
        # for i in range(schedule.start_page, schedule.start_page + 5):
        for i in range(schedule.start_page, schedule.end_page + 1):
            f.write(f"\n\n$ PAGE {i + 1}\n\n")
            f.write(reader.pages[i].extract_text(visitor_text=visitor))
