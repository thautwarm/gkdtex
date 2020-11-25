from gkdtex.interpreter import Interpreter, Span, eval_to_string, CBVFunction, CBNFunction, get_raw_from_span
from gkdtex.parse import *
from gkdtex.wrap import parse
import io

interpreter = Interpreter()
PY_NAMESPACE = 'py_namespace'

def _init_py_ns(self: Interpreter):
    """
    init a python namespace of the interpreter for later python exec and eval
    """
    self.state[PY_NAMESPACE] = {'self': self}

Interpreter.initializers.append(_init_py_ns)

def register_pyfunc(n):
    def _(f):
        interpreter.globals[n] = f
        return f
    return _


@register_pyfunc("Verb")
@register_pyfunc("verb")
def verb(self: Interpreter, spans, tex_print, _):
    r"""
    '\verb{ {1, 2, 3} }' -> ' {1, 2, 3} '
    """
    span = spans[0]
    if not isinstance(span, Span):
        return
    src = span.src
    l, r = span.offs
    contents = src[l:r]
    possible_delimiters = ('&', '-', '+', '!', '^', '#', '@', ':', '"', ';', '|')
    for e in possible_delimiters:
        if e in contents:
            continue
        tex_print('\\Verb')
        tex_print(e)
        tex_print(contents)
        tex_print(e)
        return
    raise ValueError("you contents ({} ...) have all candidate"
                     "delimiters({})".format(contents[:50], ', '.join(map(repr, possible_delimiters))))


@register_pyfunc("argsrc")
def argsrc(self: Interpreter, _, tex_print, arg):
    r"""
    '\argsrc{#\0}' -> the verbatim content of arg 0.
    '\argsrc{#\a}' -> the verbatim content of arg 'a'.

    \define{\a{^x}{^y}}{
        \argsrc{#\x} + #\y
    }
    \a{1 +  1\a}{2}
    ->
    1 +  1\a + 2
    P.S: the return will not expand again, unless you manually expand it.
    """
    if isinstance(arg, Seq):
        arg = arg.xs[0]

    assert isinstance(arg, Arg)
    argname = arg.arg
    level = arg.level
    # get the parent frame
    _, spans, _, names_offset = self.frames[level]
    if isinstance(argname, int):
        span = spans[argname - 1]
    else:
        span = spans[names_offset[argname]]
    if not span:
        return
    l, r = span.offs
    tex_print(span.src[l:r])

@register_pyfunc("define")
def define(self: Interpreter, spans, tex_print, sig, body):
    r"""
    define call-by-value command
    \define{\a{^a}{^b}}{
        #\a(or #\1)  #\b(or #\2)
    }
    """
    if isinstance(sig, Seq):
        sig = sig.xs[0]

    assert isinstance(sig, Command)
    string_io = io.StringIO()

    if sig.cmd in self.globals:
        raise NameError("Redefinition of \\{}".format(sig.cmd))

    if sig.args is None:
        self.interp(string_io.write, body)
        self.globals[sig.cmd] = string_io.getvalue()
        return

    defaults = []
    name_offsets = {}
    default_spans = []

    for off, each in enumerate(sig.args):
        if isinstance(each, KwGroup):
            name_offsets[each.kw] = off
        if each.obj is not None:
            defaults.append(eval_to_string(self, each.obj))
        else:
            defaults.append(None)

        default_spans.append(Span(self.src, each.offs))

    self.globals[sig.cmd] = CBVFunction(defaults, default_spans, name_offsets, body)



@register_pyfunc("defineLazy")
def define(self: Interpreter, spans, tex_print, sig, body):
    r"""
    define call-by-value command
    \define{\a{^a}{^b}}{
        #\a(or #\1)  #\b(or #\2)
    }
    """
    if isinstance(sig, Seq):
        sig = sig.xs[0]

    assert isinstance(sig, Command)
    string_io = io.StringIO()

    if sig.cmd in self.globals:
        raise NameError("Redefinition of \\{}".format(sig.cmd))

    if sig.args is None:
        self.interp(string_io.write, body)
        self.globals[sig.cmd] = string_io.getvalue()
        return

    defaults = []
    name_offsets = {}
    default_spans = []

    for off, each in enumerate(sig.args):
        if isinstance(each, KwGroup):
            name_offsets[each.kw] = off
        if each.obj is not None:
            defaults.append(eval_to_string(self, each.obj))
        else:
            defaults.append(None)

        default_spans.append(Span(self.src, each.offs))

    self.globals[sig.cmd] = CBNFunction(defaults, default_spans, name_offsets, body)


@register_pyfunc("pyexec")
def pyexec(self: Interpreter, spans, tex_print, _, expr):
    span = spans[0] # type:Span
    l, r = span.offs
    options = span.src[l:r]
    ns = self.state[PY_NAMESPACE]
    ns['tex_print'] = tex_print
    options = eval('dict(' + options + ')', ns)
    if options.get('expandbefore'):
        code = eval_to_string(self, expr)
    else:
        code = get_raw_from_span(spans[1])
    exec(code.strip(), ns)

@register_pyfunc("pyeval")
def pyeval(self: Interpreter, spans, tex_print, _, expr):
    span = spans[0] # type:Span
    l, r = span.offs
    options = span.src[l:r]
    ns = self.state[PY_NAMESPACE]
    ns['tex_print'] = tex_print
    options = eval('dict(' + options + ')', ns)
    if options.get('expandbefore'):
        code = eval_to_string(self, expr)
    else:
        code = get_raw_from_span(spans[1])
    result = str(eval(code.strip(), ns))

    if options.get("expandafter"):
        result = parse(result, '<eval>')
        self.interp(tex_print, result)
    else:
        tex_print(result)
