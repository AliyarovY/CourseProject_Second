from math import ceil
from re import search
from beast_cache_wrap import beast_cache
from select_sorted import select_sorted


@beast_cache
def get_by_date(name=None, date=None, filename='dump.csv') -> None:
    if all((x == None for x in (name, date))):
        raise Exception('Miss name and date')

    if date and not name:
        fw = open(filename, 'w')
        fw.writelines(res := date_only(date))
        fw.close()
        return res

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
        cn, r, l = lnn // 2, lnn - 1, 0

        # MAIN SEARCH
        for _ in iter(bool, 111):

            line = lines[cn]
            cn_name = line.split(',')[-1].strip()

            if name == cn_name:
                break

            if name < cn_name:
                r, cn = cn, cn // 2

            if name > cn_name:
                l, cn = cn, cn + ceil((r - cn) / 2)

        res = []
        if date in line and cn_name == name:
            w_ff.write(line)
            res.append(line)

        # search name ahead
        for i in range(cn + 1, len(lines)):
            line = lines[i]

            if name not in line:
                break

            if name != date:
                if date in line:
                    w_ff.write(lines[i])
                    res.append(lines[i])

            if date == name:
                if name == lines[i].split(',')[-1].strip():
                    w_ff.write(lines[i])
                    res.append(lines[i])
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
                    res.append(lines[i])

            if date == name:
                if name == lines[i].split(',')[-1].strip():
                    w_ff.write(lines[i])
                    res.append(lines[i])
                else:
                    break




def date_only(date):
    search(r'\d{4}(-\d{2}){2}', date).group(0)
    lines = select_sorted(sort_columns=["date"], limit=600_000, group_by_name=False, order='asc', filename=None)
    need_date = int(''.join(date.split('-')))
    cn_date = ''
    cn, r, l = len(lines) // 2, len(lines), 0
    rr = []

    while  date not in lines[cn]:
        cn_date = int(''.join(lines[cn].split(',')[0].split('-')))
        if cn_date > need_date:
            cn, r = cn // 2, cn
        else:
            cn, l = ceil(cn + (r - cn) / 2), cn
    rr.append(lines[cn])

    for j in '-+':
        i = eval(f'{cn}{j}1')

        try:
            while date in lines[i]:
                line = lines[i]
                rr.append(line)
                i = eval(f'{i} {j} 1')

        except:
            continue

    return rr



def branch():
    date = input('Дата в формате yyyy-mm-dd [all]: ') or None
    name = input('Тикер [all]: ') or None
    file = input('Файл dump.csv: ') or 'dump.cvs'
    get_by_date(name, date, file)



