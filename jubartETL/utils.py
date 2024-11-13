


def get_mark(product, marks):
    list_values = [s for s in marks if s in product]
    result = None
    result_len = 0
    for val in list_values:
        if len(val) > result_len:
            result_len = len(val)
            result = val
    return result

