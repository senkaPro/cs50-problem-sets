def lines(a, b):
    """Return lines in both a and b"""
    # set of unique similar lines
    uniq = set()
    # list of sentences in a
    lst_1 = a.split('\n')
    # list of sentences in b
    lst_2 = b.split('\n')

    # loop throught the list a and make cash of sentences
    for line in lst_1:
        lst = []
        lst.append(line)
        # loop throught the list b and check every sentence against the list a cash
        for line1 in lst_2:
            if line1 in lst:
                # if line is in the cash of a means they both similar
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
