from math import ceil
from re import search


def get_by_date(date: str, name: str, filename='dump.csv') -> None:
    is_correct_date = search(r'\d{4}(-\d{2}){2}', date).group(0)
    assert is_correct_date == date
    is_correct_name = search(r'[A-Z]+', name).group(0)
    assert is_correct_name == name

    with open('all_stocks_5yr.csv') as ff, open(filename, 'a') as w_ff:
        lines = ff.readlines()
        int_date = int(''.join(date.split('-')))
        lnn = len(lines)
        cn, r, l = lnn // 2, lnn - 1, 1

        # MAIN SEARCH
        while lines[cn].split(',')[0] != date:

            cn_date = int(''.join(lines[cn].split(',')[0].split('-')))

            if int_date < cn_date:
                r, cn = cn, cn // 2

            if int_date > cn_date:
                l, cn = cn, cn + ceil((r - cn) / 2)

        if all([x in lines[cn] for x in [date, name]]):
            w_ff.write(lines[cn])

        # search name ahead
        for i in range(cn + 1, len(lines)):
            if date not in lines[i]:
                break
            if name in (res := lines[i]):
                w_ff.write(res)
        # search name from behind
        for i in range(cn - 1, -1, -1):
            if date not in lines[i]:
                break
            if name in (res := lines[i]):
                w_ff.write(res)
