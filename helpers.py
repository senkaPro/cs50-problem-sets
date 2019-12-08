from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    # set of unique similar lines
    uniq = set()
    # list of sentences in a
    lst_1 = a.split('\n')
    # list of sentences in b
    lst_2 = b.split('\n')

    # loop throught the list a
    for line in lst_1:
        # loop throught the list b and check every sentence against the list a
        for line1 in lst_2:
            if line1 == line:
                # add matching lines in unique sentences
                uniq.add(line1)

    return list(uniq)


def sentences(a, b):
    """Return sentences in both a and b"""
    # set of unique english sentences
    uniq = set()

    lst_a = sent_tokenize(a)
    lst_b = sent_tokenize(b)

    for sentence in lst_a:
        for sentence1 in lst_b:
            if sentence1 == sentence:
                uniq.add(sentence1)

    return list(uniq)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    uniq = set()

    for i in range(len(a)):
        for j in range(n):
            lst = []
            lst.append(a[j:n])
            for k in range(len(b)):
                for l in range(n):
                    sub_str = b[k:l]
                    if sub_str in lst:
                        uniq.add(sub_str)

    return list(uniq)
