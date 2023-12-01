debugMode = False


def reverse_str(s):
    return "".join(reversed(s))


def dprint(v, *args, **kwargs):
    if debugMode:
        print(v, args, kwargs)

