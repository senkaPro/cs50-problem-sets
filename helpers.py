def lines(a, b):
    """Return lines in both a and b"""
    # set of unique similar lines
    uniq = set()
    # list of sentences in a
    lst_1 = a.split('\n')
    # list of sentences in b
    lst_2 = b.split('\n')

    # loop throught the sentences in b and if same sentence in a add it to unique
    for line in lst_2:
        if line in lst_1:
            uniq.add(line)

    return list(uniq)


def sentences(a, b):
    """Return sentences in both a and b"""

    # TODO
    return []


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # TODO
    return []
