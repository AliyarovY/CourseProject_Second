from re import match
from shell_sort import shell_sort
from beast_cache_wrap import beast_cache


def select_sorted(sort_columns=["Name"], limit=10, order='asc', filename='dump.csv', group_by_name=False):
    stock = []
    '''CHECK SORT_COLUMNS'''
    vv = {'high', 'date', 'open', 'low', 'close', 'volume', 'name'}
    if any([x.lower() not in vv for x in sort_columns]):
        raise Exception('Incorrect sort_columns argument')

    # Correcting items in sort_columns
    for i in range(len(sort_columns)):
        j = sort_columns[i]
        sort_columns[i] = j.capitalize() if j == 'name' else j

    # Check limit value
    if not isinstance(limit, int):
        raise Exception('limit most be int')

    # Work with read file
    with open('all_stocks_5yr.csv') as file:
        file.readline()
        result_list = iter(file.readlines(46 * limit))

    '''Result Sort'''
    # Is order
    if order not in {'desc', 'asc'}:
        raise Exception('Incorrect order argument')
    # Order dict
    ord_d = dict(desc='True', asc='False')
    order = ord_d[order]

    # Check and work group_by_name
    if group_by_name not in [False, True]:
        raise Exception('Incorrect sort_columns argument')
    if group_by_name:
        try:
            sort_columns.remove('Name')
        except:
            pass
        sort_columns.insert(0, 'Name')

    # Functon for make key list
    floats = set('open high low close volume'.split())
    ind_clmns = 'date open high low close volume Name'.split()
    f_dct = {}
    for j in sort_columns:
        if j in floats:
            f_dct[j] = float
        else:
            f_dct[j] = lambda x: x

    def f_f_funcs(value):
        line = value.split(',')
        res = []
        correct = match(r'\d{4}(-\d{2}){2}.*,[A-Z]*', value).group(0)
        for j in sort_columns:
            i = ind_clmns.index(j)
            if not correct:
                stock.append(','.join(line) + '\n')
                break
            f = f_dct[j]
            current = f(line[i])
            res.append(current)
        return res

    # Main Sort
    result_list = sorted(result_list, key=f_f_funcs, reverse=eval(order)) + stock
    '''Write in file'''
    if filename:
        with open(filename, 'w') as dump_file:
            dump_file.writelines(list(result_list))

    return result_list


@beast_cache
def select_sorted_with_cache(sort_columns=["Name"], limit=10, group_by_name=False, order='asc', filename='dump.csv'):
    return select_sorted(sort_columns=sort_columns, limit=limit, group_by_name=group_by_name, order=order,
                         filename=filename)


def orr(os, tr, ex):
    tp = type(ex)
    try:
        exec(f'global {os}; {os} = {tr} or {ex}')
    except:
        if tp == str:
            exec(f'global {os}; {os} = {repr(f"{ex}")}')
        else:
            exec(f'global {os}; {os} = {ex}')


def main():
    print('''
Сортировать по цене
открытия (1)
закрытия (2)
максимум [3]
минимум (4)
объем (5)
''', end=': ')
    orr('srt_clm', "'open close high low volume'.split()[int(input()) - 1]", ["Name"])
    orr('order', "'asc desc'.split()[int(input('Порядок по убыванию [1] / возрастанию (2): ')) - 1]", 'asc')
    orr('limit' , "int(input('Ограничение выборки [10]: '))", 10)
    orr('filename', "input('Название файла для сохранения результата [dump.csv]: ')" ,'dump.cvs')
    select_sorted(srt_clm, limit,  order, filename, group_by_name=False,)
