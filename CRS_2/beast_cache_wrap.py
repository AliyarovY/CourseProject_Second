import json


def beast_cache(func):
    def ff(*args, **kwargs):
        try:
            with open('l_cache', 'r') as file:
                cache_stock = json.load(file)
        except:
            with open('l_cache', 'w') as file:
                file.write('{}')
            with open('l_cache', 'r') as file:
                cache_stock = json.load(file)

        key = func.__name__ + str(args) + str(kwargs)


        if key not in cache_stock:
            with open('l_cache', 'w') as file:
                result = func(*args, **kwargs)
                cache_stock[key] = result
                json.dump(cache_stock, file, indent=4)
                return result

        return cache_stock[key]

    ff.file_name = f'{func.__name__}_cache'

    return ff



