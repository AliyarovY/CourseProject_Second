from math import ceil
from re import search


def get_by_date(name: str, date=None, filename='dump.csv') -> None:
    name = name.upper()
    date = date or name
    if date is name:
        is_correct_date = search(r'[A-Z]+', date).group(0)
    else:
        is_correct_date = search(r'\d{4}(-\d{2}){2}', date).group(0)

    assert is_correct_date == date
    is_correct_name = search(r'[A-Z]+', name).group(0)
    assert is_correct_name == name

    with open('all_stocks_5yr.csv') as ff, open(filename, 'a') as w_ff:
        lines = ff.readlines()
        lnn = len(lines)
        cn, r, l = lnn // 2, lnn - 1, 1

        # MAIN SEARCH
        while True:

            line = lines[cn]
            cn_name = line.split(',')[-1].strip()

            if name == cn_name:
                break

            if name < cn_name:
                r, cn = cn, cn // 2

            if name > cn_name:
                l, cn = cn, cn + ceil((r - cn) / 2)

        if date in line and cn_name == name:
            w_ff.write(line)

        # search name ahead
        for i in range(cn + 1, len(lines)):
            line = lines[i]

            if name not in line:
                break

            if name != date:
                if date in line:
                    w_ff.write(lines[i])

            if date == name:
                if name == lines[i].split(',')[-1].strip():
                    w_ff.write(lines[i])
                else:
                    break

        # search name from behind
        for i in range(cn - 1, -1, -1):
            line = lines[i]

            if name not in line:
                break

            if name != date:
                if date in line:
                    w_ff.write(lines[i])

            if date == name:
                if name == lines[i].split(',')[-1].strip():
                    w_ff.write(lines[i])
                else:
                    break


get_by_date('RRC')
