def ljust(s, width=3):
    return str(s).ljust(width, " ")


def rjust(s, width=3):
    return str(s).rjust(width, " ")


def nice_int(n, width=3):
    return str(int(n)).rjust(width, " ")
