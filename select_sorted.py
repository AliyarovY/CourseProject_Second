from re import match
from shell_sort import shell_sort
from beast_cache_wrap import beast_cache


@beast_cache
def select_sorted(sort_columns=["Name"], limit=10, group_by_name=False, order='asc', filename='dump.csv'):
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
        correct = match(r'\d{4}(-\d{2}){2}(,\d+?\.?\d*?){5},[A-Z]*\n', value).group(0)
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
    result_list = shell_sort(result_list, key=f_f_funcs, reverse=eval(order)) + stock
    '''Write in file'''
    with open(filename, 'w') as dump_file:
        dump_file.writelines(list(result_list))

    return result_list


