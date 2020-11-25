from gkdtex.parse import (
    Seq, Arg, PosGroup, KwGroup, Command, Object, Whitespace,
    Block, Subscript, Superscript
)
from gkdtex.wrap import parse
from gkdtex.spelling import number_spelling
from collections import deque
from contextlib import contextmanager
import io
import typing
import sys


class Span:
    __slots__ = ['offs', 'src']
    def __init__(self, src: str, offs: typing.Tuple[int, int]):
        self.src = src
        self.offs = offs


class CBVFunction:
    """
    interpreted call by value functions
    """
    def __init__(self,
                 defaults: list,
                 default_spans: typing.List[typing.Optional[Span]],
                 name_offsets: typing.Dict[str, int], obj: Object):
        self.body = obj
        self.defaults = defaults
        self.name_offsets = name_offsets
        self.default_spans = default_spans

class CBNFunction:
    """
    interpreted call by name functions
    """
    def __init__(self,
                 defaults: list,
                 default_spans: typing.List[typing.Optional[Span]],
                 name_offsets: typing.Dict[str, int], obj: Object):
        self.body = obj
        self.defaults = defaults
        self.name_offsets = name_offsets
        self.default_spans = default_spans


class Interpreter:
    initializers = []
    def __init__(self):
        ### Commands
        self.globals = dict()

        ### Contextual Fields
        self.filename = None
        self.src = None

        self.state = {}

        ### The Frames field has a constant reference.
        self.frames = deque() # type: typing.Deque[tuple[str, list[typing.Optional[Span]], list[Object], dict[str, int]]]

    def initialize(self):
        for each in self.initializers:
            each(self)

    def _load_src(self):
        if self.src is None:
            with open(self.filename) as f:
                self.src = f.read()

    @contextmanager
    def change_file(self, filename):
        old_filename, self.filename = self.filename, filename
        src, self.src = self.src, None
        try:
            self.filename = filename
            self._load_src()
            yield
        finally:
            self.src = src
            self.filename = old_filename


    def run_file(self, filename, tex_print=sys.stdout.write):
        with self.change_file(filename):
            src, filename = self.src, self.filename
            obj = parse(src, filename)
            self.interp(tex_print, obj)


    def interp_many(self, tex_print, objs: typing.List[Object]):
        i = self.__class__.interp
        for each in objs:
            i(self, tex_print, each)


    def interp(self, tex_print, obj: Object):
        if isinstance(obj, Whitespace):
            tex_print(obj.text)
        elif isinstance(obj, str):
            tex_print(obj)
        elif isinstance(obj, Seq):
            self.interp_many(tex_print, obj.xs)
        elif isinstance(obj, Subscript):
            self.interp(tex_print, obj.a)
            tex_print('_')
            self.interp(tex_print, obj.a)
        elif isinstance(obj, Superscript):
            self.interp(tex_print, obj.a)
            tex_print('^')
            self.interp(tex_print, obj.a)

        elif isinstance(obj, Block):
            tex_print('{')
            self.interp(tex_print, obj.obj)
            tex_print('}')
        elif isinstance(obj, Arg):
            argoff = obj.arg
            cmd, _, arguments, names = self.frames[obj.level]

            if isinstance(argoff, str):
                argoff = names[argoff]
                assert isinstance(argoff, int)
            else:
                assert isinstance(argoff, int)
                argoff -= 1
            try:
                val = arguments[argoff]
            except IndexError:
                raise IndexError("\\{} doesn't have {} argument".format(cmd, number_spelling(1 + argoff)))
            if isinstance(val, str):
                tex_print(val)
            else:
                assert callable(val)
                val(self, tex_print)

        elif isinstance(obj, Command):

            f = self.globals.get(obj.cmd)
            if f is None:
                tex_print('\\' + obj.cmd)
                if obj.args is not None:
                    for arg in obj.args:
                        tex_print('{')
                        if isinstance(arg, KwGroup):
                            raise ValueError("latex command \\{} "
                                             "cannot use keyword argument {!r}".format(obj.cmd, arg.kw))
                        if arg.obj is not None:
                            self.interp(tex_print, arg.obj)
                        tex_print('}')
                return
            if isinstance(f, str):
                if obj.args is not None:
                    raise TypeError("\\" + obj.cmd, 'cannot accept arguments.')
                tex_print(f)

            elif isinstance(f, CBVFunction):
                args = obj.args or []
                arg_io = io.StringIO()
                arguments = f.defaults.copy()
                spans = f.default_spans.copy()
                name_offsets = f.name_offsets
                src = self.src
                for off, arg in enumerate(args):
                    if isinstance(arg, KwGroup):
                        try:
                            off = name_offsets[arg.kw]
                        except KeyError:
                            raise ValueError("\\{} has no keyword argument {}".format(obj.cmd, arg.kw))

                    if arg.obj is not None:
                        self.interp(arg_io.write, arg.obj)
                        arguments[off] = arg_io.getvalue()
                        arg_io.seek(0)
                        arg_io.truncate(0)

                    spans[off] = Span(src, arg.offs)
                if any(a is None for a in arguments):
                    raise ValueError("Invalid call of \\{}, {} argument is not given".format(obj.cmd, number_spelling(1 + arguments.index(None))))

                self.frames.appendleft((obj.cmd, spans, arguments, f.name_offsets))
                self.interp(tex_print, f.body)
                self.frames.popleft()
                return
            elif isinstance(f, CBNFunction):
                args = obj.args or []
                arguments = f.defaults.copy()
                spans = f.default_spans.copy()
                name_offsets = f.name_offsets
                src = self.src
                for off, arg in enumerate(args):
                    if isinstance(arg, KwGroup):
                        try:
                            off = name_offsets[arg.kw]
                        except KeyError:
                            raise ValueError("\\{} has no keyword argument {}".format(obj.cmd, arg.kw))

                    # noinspection PyDefaultArgument
                    if arg.obj:
                        def lazy(self, tex_print, obj=arg.obj):
                            self.interp(tex_print, obj)

                        arguments[off] = lazy
                    spans[off] = Span(src, arg.offs)

                if any(a is None for a in arguments):
                    raise ValueError("Invalid call of \\{}, {} argument is not given".format(obj.cmd, number_spelling(1 + arguments.index(None))))

                self.frames.appendleft((obj.cmd, spans, arguments, f.name_offsets))
                self.interp(tex_print, f.body)
                self.frames.popleft()
                return
            else:  # py callable. Do not use keyword arguments
                args = obj.args or []
                assert callable(f)
                arguments = []
                spans = []
                src = self.src
                for arg in args:
                    if isinstance(arg, KwGroup):
                        raise ValueError("\\{} is a Python callable, "
                                         "cannot accept keyword argument({}).".format(obj.cmd, arg.kw))
                    if arg.obj is None:
                        raise ValueError("\\{} is Python callable, whose {}"
                                         "argument cannot be null.".format(obj.cmd, number_spelling(len(arguments))))
                    arguments.append(arg.obj)
                    spans.append(Span(src, arg.offs))

                f(self, spans, tex_print, *arguments)

        else:
            raise TypeError(obj)


def eval_to_string(interpreter: Interpreter, o: Object):
    if isinstance(o, Seq) and not o.xs or isinstance(o, Whitespace):
        return ''
    string_io = io.StringIO()
    interpreter.interp(string_io.write, o)
    return string_io.getvalue()

def get_raw_from_span(span: Span):
    if not span:
        return ''
    l, r = span.offs
    return span.src[l:r]