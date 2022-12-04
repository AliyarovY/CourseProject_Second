def shell_sort(ls: list, key=lambda x: x, reverse=False) -> None:
    if not hasattr(ls, '__iter__') or isinstance(ls, str):
        return ls

    ls = list(ls)
    grap = len(ls) // 2
    is_double = False

    while grap > 1:
        i = 0

        while i < (len(ls) - (grap)):
            left = ls[i]
            right = ls[i + grap]

            if key(left) == key(right):
                i += 1
                continue

            if not isinstance(ls[i], str):
                ls[i], ls[i + grap] = comparison('min', left, right, key=key), comparison('max', left, right, key=key)
            else:
                if key(ls[i]) > key(ls[i + grap]):
                    ls[i], ls[i + grap] = ls[i + grap], ls[i]

            i += 1

        grap //= 2

    if grap <= 1:
        grap = 1
        while True:
            for i in range(len(ls) - 1):

                left = ls[i]
                right = ls[i + grap]

                if key(left) > key(right):
                    ls[i], ls[i + grap] = ls[i + grap], ls[i]
                    is_double = True

            if is_double:
                is_double = False
            else:
                break

    if reverse:
        ls = my_reverse(ls)
    return ls


def my_reverse(obj):
    if not hasattr(obj, '__iter__'):
        raise Exception('Nice Try ggwp')

    for i in range(len(obj) // 2):
        obj[i], obj[~i] = obj[~i], obj[i]

    return obj


def unpack(it, result=[]) -> list:
    if not hasattr(it, '__iter__') or isinstance(it, str):
        result.append(it)
        return

    for j in it:
        unpack(j)

    return result


def comparison(is_, *args, key=lambda x: x, unpackk=False) -> list:
    if not args:
        return None
    _is = ['min', 'max']
    if is_ not in _is:
        raise Exception('man ...')
    if unpackk:
        args = unpack(args)
    _is = {k: v for k, v in zip(_is, '<>')}
    res = args[0]
    for j in args:
        if eval(f'{key(j)} {_is[is_]} {key(res)}'):
            res = j
    args = ()
    return res
