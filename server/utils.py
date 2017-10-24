


def clamp(val, lower, upper):
    """ val if it's between lower and upper, else the closest of the two"""
    return min(max(val, lower), upper)


def concat(arr):
    """Takes a list of sequences, returns the concatenation of the sequences """
    if isinstance(arr[0], str):
        return "".join(arr)
    if isinstance(arr[0], bytes):
        return b"".join(arr)
    if isinstance(arr[0], list):
        l = []
        for s in arr:
            l += s
        return l
    if isinstance(arr[0], tuple):
        l = []
        for s in arr:
            l += s
        return tuple(l)
    else:
        raise ValueError("type {} can't be concatenated".format(type(arr[0])))
