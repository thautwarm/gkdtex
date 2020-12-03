import warnings
warnings.filterwarnings('ignore', category=SyntaxWarning, message='"is" with a literal')

from gkdtex.parse import *
from gkdtex.lex import *

_parse = mk_parser()


def parse(text: str, filename: str = "unknown"):
    tokens = lexer(filename, text)
    status, res_or_err = _parse(None, Tokens(tokens))
    if status:
        return res_or_err

    msgs = []
    lineno = None
    colno = None
    filename = None
    offset = 0
    msg = ""
    for each in res_or_err:
        i, msg = each
        token = tokens[i]
        lineno = token.lineno + 1
        colno = token.colno
        offset = token.offset
        filename = token.filename
        break
    e = SyntaxError(msg)
    e.lineno = lineno
    e.colno = colno
    e.filename = filename
    e.text = text[offset - colno:text.find('\n', offset)]
    e.offset = colno
    raise e
