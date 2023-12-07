import re

text = ""
with open("txts/berkeley_city_college-2023-fall.txt", encoding="utf-8") as f:
    text = f.read()

pages = re.split(r"\n\n\$", text)
lines = pages[4].split("\n")
for i, line in enumerate(lines):
    lineno = str(i).rjust(3, "0")
    print(f"{lineno} | {line}")
