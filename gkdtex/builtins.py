from gkdtex.developer_utilities import *
from gkdtex.wrap import parse
import io

PY_NAMESPACE = 'py_namespace'

def _init_py_ns(self: Interpreter):
    """
    init a python namespace of the interpreter for later python exec and eval
    """
    self.state[PY_NAMESPACE] = {'self': self}

Interpreter.default_initializers.append(_init_py_ns)

def register_pyfunc(n):
    def _(f):
        Interpreter.default_globals[n] = f
        return f
    return _


@register_pyfunc("gkd@Verb")
@register_pyfunc("gkd@verb")
def verb(arg: Group, *, self: Interpreter, tex_print):
    r"""
    '\verb{ {1, 2, 3} }' -> ' {1, 2, 3} '
    """
    src = self.src
    if not arg.offs:
        return
    contents = get_raw_from_span(Span(src, arg.offs))
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


@register_pyfunc("gkd@argsrc")
def argsrc(arg: Group, *, self: Interpreter, tex_print):
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
    arg = arg.obj
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
    tex_print(get_raw_from_span(span))

@register_pyfunc("gkd@def")
def define(sig: Group, body: Group, *, self: Interpreter, tex_print):
    r"""
    define call-by-value command
    \gkd@def{\a{^a}{^b}}{
        #\a(or #\1)  #\b(or #\2)
    }
    """
    sig = sig.obj
    body = body.obj
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



@register_pyfunc("gkd@def@lazy")
def define(sig: Group, body: Group, *, self: Interpreter, tex_print):
    r"""
    define call-by-value command
    \gkd@def@lazy {\a{^a}{^b}}{
        #\a(or #\1)  #\b(or #\2)
    }
    """
    sig = sig.obj
    body = body.obj

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


@register_pyfunc("gkd@pyexec")
def pyexec(expr: Group, *, self: Interpreter, tex_print, expand:Group = None):
    ns = self.state[PY_NAMESPACE]
    ns['tex_print'] = tex_print
    if expand:
        expand = get_raw_from_span_params(self.src, expand.offs)
        expand = eval('dict(' + expand + ')', ns)
    else:
        expand = {}

    if expand.get('before'):
        code = eval_to_string(self, expr.obj)
    else:
        code = get_raw_from_span_params(self.src, expr.offs)
    exec(code.strip(), ns)

@register_pyfunc("gkd@pyeval")
def pyeval(expr:Group, *, self: Interpreter, tex_print, expand:Group = None):
    ns = self.state[PY_NAMESPACE]
    ns['tex_print'] = tex_print
    if expand:
        expand = get_raw_from_span_params(self.src, expand.offs)
        expand = eval('dict(' + expand + ')', ns)
    else:
        expand = {}

    if expand.get('before'):
        code = eval_to_string(self, expr.obj)
    else:
        code = get_raw_from_span_params(self.src, expr.offs)
    result = str(eval(code.strip(), ns))

    if expand.get("after"):
        result = parse(result, '<eval>')
        self.interp(tex_print, result)
    else:
        tex_print(result)


@register_pyfunc("gkd@usepackage")
def using(package: Group, *, self: Interpreter, tex_print):
    from importlib import import_module
    packagename = get_raw_from_span_params(self.src, package.offs).strip()
    m = import_module("{}".format(packagename))
    gkd_interface = getattr(m, 'GkdInterface', None)
    if gkd_interface is None:
        raise ValueError("Python module {} doesn't implement its GkdInterface.".format(packagename))

    loader = getattr(gkd_interface, 'load', None)
    if loader is None:
        raise ValueError("{} hasn't provided a 'load' function.".format(packagename))
    loader(self, tex_print)
    disposer = getattr(gkd_interface, 'dispose', None)
    if disposer is not None:
        self.disposers.append(lambda self: disposer(self, tex_print))

@register_pyfunc("gkd@input")
def input_file(filename: Group, self: Interpreter, tex_print):
    from pathlib import Path
    path = get_raw_from_span_params(self.src, filename.offs).strip()
    path = str(Path(self.filename).parent / path)
    self.run_file(path, tex_print)
