indicator = {
    1: 'st',
    2: 'nd',
    3: 'rd'
}
direct = {
    11: '11-th',
    12: '12-th',
    13: '13-th',
}
def number_spelling(i):
    o = direct.get(i)
    if o:
        return o
    return '{}-{}'.format(i, indicator.get(i % 10, 'th'))
