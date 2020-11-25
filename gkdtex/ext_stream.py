import io
import os

WS = object()
COMMAND = object()


def read_stream(f: io.TextIOWrapper, filename: str):
    word = io.StringIO()
    stringio_write = io.StringIO.write
    stringio_trunc = io.StringIO.truncate
    stringio_seek = io.StringIO.seek
    stringio_getvalue = io.StringIO.getvalue
    linesep = os.linesep

    VERBATIM_STATUS = 0
    LINENO = 1
    COLNO = 2
    state = [
        False, # verbatim,
        1,
        1,
        filename
    ]

    while ch := f.read(1):
        if ch.isspace():
            if ch == linesep:
                state[LINENO] += 1
                state[COLNO] = 1
            else:
                state[COLNO] += 1
            if state[VERBATIM_STATUS]:
                stringio_write(word, ch)
            else:
                yield stringio_getvalue(word), state

                stringio_seek(word, 0)
                stringio_trunc(word, 0)
        else:
            state[COLNO] += 1
            stringio_write(word, ch)

    yield stringio_getvalue(word), state

if __name__ == '__main__':
    for e in read_stream(io.StringIO("aaaaa aaaa aaa "), "file"):
        print(e)
