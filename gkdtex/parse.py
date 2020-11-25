
"""
Copyright thautwarm (c) 2019

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

    * Neither the name of thautwarm nor the names of other
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import typing

class Whitespace:
    __slots__ = ['text']
    def __init__(self, text: str):
        self.text = text

class PosGroup:
    __slots__ = ['offs', 'obj']

    def __init__(self, loff: int, obj: 'typing.Optional[Object]', roff: int):
        self.offs = (loff, roff)
        self.obj = obj

class KwGroup:
    __slots__ = ['offs', 'kw', 'obj']

    def __init__(self, loff: int, kw: str, obj: 'typing.Optional[Object]' , roff: int):
        self.offs = (loff, roff)
        self.obj = obj
        self.kw = kw

Group = typing.Union[KwGroup, PosGroup]
class Command:
    def __init__(self, cmd: str, args: typing.Optional[typing.List[Group]]):
        self.cmd = cmd
        self.args = args

class Arg:
    def __init__(self, level: int, arg: typing.Union[str, int]):
        self.level = level
        self.arg = arg

class Seq:
    def __init__(self, xs: typing.List['Object']):
        self.xs = xs

class Subscript:
    def __init__(self, a: 'Object', b: 'Object'):
        self.a = b
        self.a = b

class Superscript:
    def __init__(self, a: 'Object', b: 'Object'):
        self.a = b
        self.a = b

class Block:
    def __init__(self, obj: 'Object'):
        self.obj = obj

def mkArg(a):
    if isinstance(a, str):
        return '#' + a
    return Arg(*a)

def Text(x: str) -> str:
    return x

Object = typing.Union[str, Seq, Arg, Command, Whitespace, Block, Subscript, Superscript]

def arg_level_up(x):
    if isinstance(x, str):
        return '#' + x
    level, arg = x
    return level+1, arg

def control(x):
    return '\\' + x

def add1(x):
    return x + 1
from typing import Generic, TypeVar
T = TypeVar('T')

class Tokens():
    __slots__ = ['array', 'offset']

    def __init__(self, array):
        self.array = array
        self.offset = 0

class State():

    def __init__(self):
        pass

class AST(Generic[T]):
    __slots__ = ['tag', 'contents']

    def __init__(self, tag: str, contents: T):
        self.tag = tag
        self.contents = contents

class Nil():
    nil = None
    __slots__ = []

    def __init__(self):
        if (Nil.nil is None):
            Nil.nil = self
            return
        raise ValueError('Nil cannot get instantiated twice.')

    def __len__(self):
        return 0

    def __getitem__(self, n):
        raise IndexError('Out of bounds')

    @property
    def head(self):
        raise IndexError('Out of bounds')

    @property
    def tail(self):
        raise IndexError('Out of bounds')

    def __repr__(self):
        return '[]'
_nil = Nil()

class Cons():
    __slots__ = ['head', 'tail']

    def __init__(self, _head, _tail):
        self.head = _head
        self.tail = _tail

    def __len__(self):
        nil = _nil
        l = 0
        while (self is not nil):
            l += 1
            self = self.tail
        return l

    def __iter__(self):
        nil = _nil
        while (self is not nil):
            (yield self.head)
            self = self.tail

    def __getitem__(self, n):
        while (n != 0):
            self = self.tail
            n -= 1
        return self.head

    def __repr__(self):
        return repr(list(self))
try:

    def mk_pretty():
        from prettyprinter import register_pretty, pretty_call, pprint

        @register_pretty(Tokens)
        def pretty_tokens(value, ctx):
            return pretty_call(ctx, Tokens, offset=value.offset, array=value.array)

        @register_pretty(AST)
        def pretty_ast(value, ctx):
            return pretty_call(ctx, AST, tag=value.tag, contents=value.contents)
    mk_pretty()
    del mk_pretty
except ImportError:
    pass
del T, Generic, TypeVar
builtin_cons = Cons
builtin_nil = _nil
builtin_mk_ast = AST

def mk_parser():
    pass

    def rbnf_named_lr_step_Groups(rbnf_tmp_0, builtin_state, builtin_tokens):
        lcl_0 = rbnf_named_parse_Group(builtin_state, builtin_tokens)
        rbnf_named__check_1 = lcl_0
        lcl_0 = rbnf_named__check_1[0]
        lcl_0 = (lcl_0 == False)
        if lcl_0:
            lcl_0 = rbnf_named__check_1
        else:
            lcl_1 = rbnf_named__check_1[1]
            rbnf_tmp_1 = lcl_1
            lcl_1 = rbnf_tmp_0.append
            lcl_1 = lcl_1(rbnf_tmp_1)
            rbnf_tmp_1_ = rbnf_tmp_0
            lcl_2 = (True, rbnf_tmp_1_)
            lcl_0 = lcl_2
        return lcl_0

    def rbnf_named_lr_loop_Groups(rbnf_tmp_0, builtin_state, builtin_tokens):
        rbnf_named_lr_Groups_reduce = rbnf_tmp_0
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        lcl_0 = rbnf_named_lr_step_Groups(rbnf_named_lr_Groups_reduce, builtin_state, builtin_tokens)
        rbnf_named_lr_Groups_try = lcl_0
        lcl_0 = rbnf_named_lr_Groups_try[0]
        lcl_0 = (lcl_0 is not False)
        while lcl_0:
            lcl_1 = builtin_tokens.offset
            rbnf_named__off_0 = lcl_1
            lcl_1 = rbnf_named_lr_Groups_try[1]
            rbnf_named_lr_Groups_reduce = lcl_1
            lcl_1 = rbnf_named_lr_step_Groups(rbnf_named_lr_Groups_reduce, builtin_state, builtin_tokens)
            rbnf_named_lr_Groups_try = lcl_1
            lcl_1 = rbnf_named_lr_Groups_try[0]
            lcl_1 = (lcl_1 is not False)
            lcl_0 = lcl_1
        lcl_0 = builtin_tokens.offset
        lcl_0 = (lcl_0 == rbnf_named__off_0)
        if lcl_0:
            lcl_1 = (True, rbnf_named_lr_Groups_reduce)
            lcl_0 = lcl_1
        else:
            lcl_0 = rbnf_named_lr_Groups_try
        return lcl_0

    def rbnf_named_lr_step_Objects(rbnf_tmp_0, builtin_state, builtin_tokens):
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        try:
            builtin_tokens.array[(builtin_tokens.offset + 0)]
            _rbnf_peek_tmp = True
        except IndexError:
            _rbnf_peek_tmp = False
        lcl_0 = _rbnf_peek_tmp
        if lcl_0:
            lcl_2 = builtin_tokens.array[(builtin_tokens.offset + 0)]
            lcl_2 = lcl_2.idint
            if (lcl_2 == 4):
                lcl_3 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_1 = lcl_3
                lcl_3 = rbnf_named__check_1[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_1
                else:
                    lcl_4 = rbnf_named__check_1[1]
                    rbnf_tmp_1 = lcl_4
                    lcl_4 = rbnf_tmp_0.append
                    lcl_4 = lcl_4(rbnf_tmp_1)
                    rbnf_tmp_1_ = rbnf_tmp_0
                    lcl_5 = (True, rbnf_tmp_1_)
                    lcl_3 = lcl_5
                lcl_1 = lcl_3
            elif (lcl_2 == 0):
                lcl_3 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_1 = lcl_3
                lcl_3 = rbnf_named__check_1[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_1
                else:
                    lcl_5 = rbnf_named__check_1[1]
                    rbnf_tmp_1 = lcl_5
                    lcl_5 = rbnf_tmp_0.append
                    lcl_5 = lcl_5(rbnf_tmp_1)
                    rbnf_tmp_1_ = rbnf_tmp_0
                    lcl_6 = (True, rbnf_tmp_1_)
                    lcl_3 = lcl_6
                lcl_1 = lcl_3
            elif (lcl_2 == 3):
                lcl_3 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_1 = lcl_3
                lcl_3 = rbnf_named__check_1[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_1
                else:
                    lcl_6 = rbnf_named__check_1[1]
                    rbnf_tmp_1 = lcl_6
                    lcl_6 = rbnf_tmp_0.append
                    lcl_6 = lcl_6(rbnf_tmp_1)
                    rbnf_tmp_1_ = rbnf_tmp_0
                    lcl_7 = (True, rbnf_tmp_1_)
                    lcl_3 = lcl_7
                lcl_1 = lcl_3
            elif (lcl_2 == 9):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_1 = lcl_3
                lcl_3 = rbnf_tmp_0.append
                lcl_7 = rbnf_tmp_1.value
                lcl_7 = Whitespace(lcl_7)
                lcl_3 = lcl_3(lcl_7)
                rbnf_tmp_1_ = rbnf_tmp_0
                lcl_7 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_7
            elif (lcl_2 == 7):
                lcl_7 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_1 = lcl_7
                lcl_7 = rbnf_named__check_1[0]
                lcl_7 = (lcl_7 == False)
                if lcl_7:
                    lcl_7 = rbnf_named__check_1
                else:
                    lcl_8 = rbnf_named__check_1[1]
                    rbnf_tmp_1 = lcl_8
                    lcl_8 = rbnf_tmp_0.append
                    lcl_8 = lcl_8(rbnf_tmp_1)
                    rbnf_tmp_1_ = rbnf_tmp_0
                    lcl_9 = (True, rbnf_tmp_1_)
                    lcl_7 = lcl_9
                lcl_1 = lcl_7
            elif (lcl_2 == 1):
                lcl_7 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_1 = lcl_7
                lcl_7 = rbnf_named__check_1[0]
                lcl_7 = (lcl_7 == False)
                if lcl_7:
                    lcl_7 = rbnf_named__check_1
                else:
                    lcl_9 = rbnf_named__check_1[1]
                    rbnf_tmp_1 = lcl_9
                    lcl_9 = rbnf_tmp_0.append
                    lcl_9 = lcl_9(rbnf_tmp_1)
                    rbnf_tmp_1_ = rbnf_tmp_0
                    lcl_10 = (True, rbnf_tmp_1_)
                    lcl_7 = lcl_10
                lcl_1 = lcl_7
            elif (lcl_2 == 2):
                lcl_10 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_1 = lcl_10
                lcl_10 = rbnf_named__check_1[0]
                lcl_10 = (lcl_10 == False)
                if lcl_10:
                    lcl_10 = rbnf_named__check_1
                else:
                    lcl_7 = rbnf_named__check_1[1]
                    rbnf_tmp_1 = lcl_7
                    lcl_7 = rbnf_tmp_0.append
                    lcl_7 = lcl_7(rbnf_tmp_1)
                    rbnf_tmp_1_ = rbnf_tmp_0
                    lcl_11 = (True, rbnf_tmp_1_)
                    lcl_10 = lcl_11
                lcl_1 = lcl_10
            else:
                lcl_10 = (rbnf_named__off_0, 'Objects lookahead failed')
                lcl_10 = builtin_cons(lcl_10, builtin_nil)
                lcl_10 = (False, lcl_10)
                lcl_1 = lcl_10
            lcl_0 = lcl_1
        else:
            lcl_1 = (rbnf_named__off_0, 'Objects got EOF')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_lr_loop_Objects(rbnf_tmp_0, builtin_state, builtin_tokens):
        rbnf_named_lr_Objects_reduce = rbnf_tmp_0
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        lcl_0 = rbnf_named_lr_step_Objects(rbnf_named_lr_Objects_reduce, builtin_state, builtin_tokens)
        rbnf_named_lr_Objects_try = lcl_0
        lcl_0 = rbnf_named_lr_Objects_try[0]
        lcl_0 = (lcl_0 is not False)
        while lcl_0:
            lcl_1 = builtin_tokens.offset
            rbnf_named__off_0 = lcl_1
            lcl_1 = rbnf_named_lr_Objects_try[1]
            rbnf_named_lr_Objects_reduce = lcl_1
            lcl_1 = rbnf_named_lr_step_Objects(rbnf_named_lr_Objects_reduce, builtin_state, builtin_tokens)
            rbnf_named_lr_Objects_try = lcl_1
            lcl_1 = rbnf_named_lr_Objects_try[0]
            lcl_1 = (lcl_1 is not False)
            lcl_0 = lcl_1
        lcl_0 = builtin_tokens.offset
        lcl_0 = (lcl_0 == rbnf_named__off_0)
        if lcl_0:
            lcl_1 = (True, rbnf_named_lr_Objects_reduce)
            lcl_0 = lcl_1
        else:
            lcl_0 = rbnf_named_lr_Objects_try
        return lcl_0

    def rbnf_named_lr_step_Script(rbnf_tmp_0, builtin_state, builtin_tokens):
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        try:
            builtin_tokens.array[(builtin_tokens.offset + 0)]
            _rbnf_peek_tmp = True
        except IndexError:
            _rbnf_peek_tmp = False
        lcl_0 = _rbnf_peek_tmp
        if lcl_0:
            lcl_2 = builtin_tokens.array[(builtin_tokens.offset + 0)]
            lcl_2 = lcl_2.idint
            if (lcl_2 == 8):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_1 = lcl_3
                lcl_3 = rbnf_named_parse_Atom(builtin_state, builtin_tokens)
                rbnf_named__check_2 = lcl_3
                lcl_3 = rbnf_named__check_2[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_2
                else:
                    lcl_4 = rbnf_named__check_2[1]
                    rbnf_tmp_2 = lcl_4
                    lcl_4 = Subscript(rbnf_tmp_0, rbnf_tmp_2)
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = (True, rbnf_tmp_1_)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 6):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_1 = lcl_3
                lcl_3 = rbnf_named_parse_Atom(builtin_state, builtin_tokens)
                rbnf_named__check_2 = lcl_3
                lcl_3 = rbnf_named__check_2[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_2
                else:
                    lcl_4 = rbnf_named__check_2[1]
                    rbnf_tmp_2 = lcl_4
                    lcl_4 = Superscript(rbnf_tmp_0, rbnf_tmp_2)
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = (True, rbnf_tmp_1_)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            else:
                lcl_3 = (rbnf_named__off_0, 'Script lookahead failed')
                lcl_3 = builtin_cons(lcl_3, builtin_nil)
                lcl_3 = (False, lcl_3)
                lcl_1 = lcl_3
            lcl_0 = lcl_1
        else:
            lcl_1 = (rbnf_named__off_0, 'Script got EOF')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_lr_loop_Script(rbnf_tmp_0, builtin_state, builtin_tokens):
        rbnf_named_lr_Script_reduce = rbnf_tmp_0
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        lcl_0 = rbnf_named_lr_step_Script(rbnf_named_lr_Script_reduce, builtin_state, builtin_tokens)
        rbnf_named_lr_Script_try = lcl_0
        lcl_0 = rbnf_named_lr_Script_try[0]
        lcl_0 = (lcl_0 is not False)
        while lcl_0:
            lcl_1 = builtin_tokens.offset
            rbnf_named__off_0 = lcl_1
            lcl_1 = rbnf_named_lr_Script_try[1]
            rbnf_named_lr_Script_reduce = lcl_1
            lcl_1 = rbnf_named_lr_step_Script(rbnf_named_lr_Script_reduce, builtin_state, builtin_tokens)
            rbnf_named_lr_Script_try = lcl_1
            lcl_1 = rbnf_named_lr_Script_try[0]
            lcl_1 = (lcl_1 is not False)
            lcl_0 = lcl_1
        lcl_0 = builtin_tokens.offset
        lcl_0 = (lcl_0 == rbnf_named__off_0)
        if lcl_0:
            lcl_1 = (True, rbnf_named_lr_Script_reduce)
            lcl_0 = lcl_1
        else:
            lcl_0 = rbnf_named_lr_Script_try
        return lcl_0

    def rbnf_named_parse_Arg(builtin_state, builtin_tokens):
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        try:
            builtin_tokens.array[(builtin_tokens.offset + 0)]
            _rbnf_peek_tmp = True
        except IndexError:
            _rbnf_peek_tmp = False
        lcl_0 = _rbnf_peek_tmp
        if lcl_0:
            lcl_2 = builtin_tokens.array[(builtin_tokens.offset + 0)]
            lcl_2 = lcl_2.idint
            if (lcl_2 == 0):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = builtin_tokens.offset
                rbnf_named__off_1 = lcl_3
                try:
                    builtin_tokens.array[(builtin_tokens.offset + 0)]
                    _rbnf_peek_tmp = True
                except IndexError:
                    _rbnf_peek_tmp = False
                lcl_3 = _rbnf_peek_tmp
                if lcl_3:
                    lcl_5 = builtin_tokens.array[(builtin_tokens.offset + 0)]
                    lcl_5 = lcl_5.idint
                    if (lcl_5 == 1):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        lcl_6 = rbnf_tmp_1.value
                        lcl_6 = int(lcl_6)
                        lcl_6 = (0, lcl_6)
                        rbnf_tmp_1_ = lcl_6
                        lcl_6 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_6
                    elif (lcl_5 == 2):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        lcl_6 = rbnf_tmp_1.value
                        lcl_6 = (0, lcl_6)
                        rbnf_tmp_1_ = lcl_6
                        lcl_6 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_6
                    else:
                        lcl_6 = (rbnf_named__off_1, 'Arg lookahead failed')
                        lcl_6 = builtin_cons(lcl_6, builtin_nil)
                        lcl_6 = (False, lcl_6)
                        lcl_4 = lcl_6
                    lcl_3 = lcl_4
                else:
                    lcl_4 = (rbnf_named__off_1, 'Arg got EOF')
                    lcl_4 = builtin_cons(lcl_4, builtin_nil)
                    lcl_4 = (False, lcl_4)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 3):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = rbnf_named_parse_Arg(builtin_state, builtin_tokens)
                rbnf_named__check_1 = lcl_3
                lcl_3 = rbnf_named__check_1[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_1
                else:
                    lcl_4 = rbnf_named__check_1[1]
                    rbnf_tmp_1 = lcl_4
                    lcl_4 = arg_level_up(rbnf_tmp_1)
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = (True, rbnf_tmp_1_)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 1):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = rbnf_tmp_0.value
                rbnf_tmp_1_ = lcl_3
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            else:
                lcl_3 = (rbnf_named__off_0, 'Arg lookahead failed')
                lcl_3 = builtin_cons(lcl_3, builtin_nil)
                lcl_3 = (False, lcl_3)
                lcl_1 = lcl_3
            lcl_0 = lcl_1
        else:
            lcl_1 = (rbnf_named__off_0, 'Arg got EOF')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_Atom(builtin_state, builtin_tokens):
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        try:
            builtin_tokens.array[(builtin_tokens.offset + 0)]
            _rbnf_peek_tmp = True
        except IndexError:
            _rbnf_peek_tmp = False
        lcl_0 = _rbnf_peek_tmp
        if lcl_0:
            lcl_2 = builtin_tokens.array[(builtin_tokens.offset + 0)]
            lcl_2 = lcl_2.idint
            if (lcl_2 == 4):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = builtin_tokens.offset
                rbnf_named__off_1 = lcl_3
                try:
                    builtin_tokens.array[(builtin_tokens.offset + 0)]
                    _rbnf_peek_tmp = True
                except IndexError:
                    _rbnf_peek_tmp = False
                lcl_3 = _rbnf_peek_tmp
                if lcl_3:
                    lcl_5 = builtin_tokens.array[(builtin_tokens.offset + 0)]
                    lcl_5 = lcl_5.idint
                    if (lcl_5 == 5):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        lcl_6 = []
                        lcl_6 = Seq(lcl_6)
                        lcl_6 = Block(lcl_6)
                        rbnf_tmp_1_ = lcl_6
                        lcl_6 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_6
                    elif (lcl_5 == 4):
                        lcl_6 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                        rbnf_named__check_1 = lcl_6
                        lcl_6 = rbnf_named__check_1[0]
                        lcl_6 = (lcl_6 == False)
                        if lcl_6:
                            lcl_6 = rbnf_named__check_1
                        else:
                            lcl_7 = rbnf_named__check_1[1]
                            rbnf_tmp_1 = lcl_7
                            try:
                                _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                if (_rbnf_cur_token.idint is 5):
                                    builtin_tokens.offset += 1
                                else:
                                    _rbnf_cur_token = None
                            except IndexError:
                                _rbnf_cur_token = None
                            lcl_7 = _rbnf_cur_token
                            rbnf_tmp_2 = lcl_7
                            lcl_7 = (rbnf_tmp_2 is None)
                            if lcl_7:
                                lcl_8 = builtin_tokens.offset
                                lcl_8 = (lcl_8, 'quote } not match')
                                lcl_8 = builtin_cons(lcl_8, builtin_nil)
                                lcl_8 = (False, lcl_8)
                                lcl_7 = lcl_8
                            else:
                                lcl_8 = Seq(rbnf_tmp_1)
                                lcl_8 = Block(lcl_8)
                                rbnf_tmp_1_ = lcl_8
                                lcl_8 = (True, rbnf_tmp_1_)
                                lcl_7 = lcl_8
                            lcl_6 = lcl_7
                        lcl_4 = lcl_6
                    elif (lcl_5 == 0):
                        lcl_6 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                        rbnf_named__check_1 = lcl_6
                        lcl_6 = rbnf_named__check_1[0]
                        lcl_6 = (lcl_6 == False)
                        if lcl_6:
                            lcl_6 = rbnf_named__check_1
                        else:
                            lcl_7 = rbnf_named__check_1[1]
                            rbnf_tmp_1 = lcl_7
                            try:
                                _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                if (_rbnf_cur_token.idint is 5):
                                    builtin_tokens.offset += 1
                                else:
                                    _rbnf_cur_token = None
                            except IndexError:
                                _rbnf_cur_token = None
                            lcl_7 = _rbnf_cur_token
                            rbnf_tmp_2 = lcl_7
                            lcl_7 = (rbnf_tmp_2 is None)
                            if lcl_7:
                                lcl_8 = builtin_tokens.offset
                                lcl_8 = (lcl_8, 'quote } not match')
                                lcl_8 = builtin_cons(lcl_8, builtin_nil)
                                lcl_8 = (False, lcl_8)
                                lcl_7 = lcl_8
                            else:
                                lcl_8 = Seq(rbnf_tmp_1)
                                lcl_8 = Block(lcl_8)
                                rbnf_tmp_1_ = lcl_8
                                lcl_8 = (True, rbnf_tmp_1_)
                                lcl_7 = lcl_8
                            lcl_6 = lcl_7
                        lcl_4 = lcl_6
                    elif (lcl_5 == 3):
                        lcl_6 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                        rbnf_named__check_1 = lcl_6
                        lcl_6 = rbnf_named__check_1[0]
                        lcl_6 = (lcl_6 == False)
                        if lcl_6:
                            lcl_6 = rbnf_named__check_1
                        else:
                            lcl_7 = rbnf_named__check_1[1]
                            rbnf_tmp_1 = lcl_7
                            try:
                                _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                if (_rbnf_cur_token.idint is 5):
                                    builtin_tokens.offset += 1
                                else:
                                    _rbnf_cur_token = None
                            except IndexError:
                                _rbnf_cur_token = None
                            lcl_7 = _rbnf_cur_token
                            rbnf_tmp_2 = lcl_7
                            lcl_7 = (rbnf_tmp_2 is None)
                            if lcl_7:
                                lcl_8 = builtin_tokens.offset
                                lcl_8 = (lcl_8, 'quote } not match')
                                lcl_8 = builtin_cons(lcl_8, builtin_nil)
                                lcl_8 = (False, lcl_8)
                                lcl_7 = lcl_8
                            else:
                                lcl_8 = Seq(rbnf_tmp_1)
                                lcl_8 = Block(lcl_8)
                                rbnf_tmp_1_ = lcl_8
                                lcl_8 = (True, rbnf_tmp_1_)
                                lcl_7 = lcl_8
                            lcl_6 = lcl_7
                        lcl_4 = lcl_6
                    elif (lcl_5 == 9):
                        lcl_6 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                        rbnf_named__check_1 = lcl_6
                        lcl_6 = rbnf_named__check_1[0]
                        lcl_6 = (lcl_6 == False)
                        if lcl_6:
                            lcl_6 = rbnf_named__check_1
                        else:
                            lcl_7 = rbnf_named__check_1[1]
                            rbnf_tmp_1 = lcl_7
                            try:
                                _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                if (_rbnf_cur_token.idint is 5):
                                    builtin_tokens.offset += 1
                                else:
                                    _rbnf_cur_token = None
                            except IndexError:
                                _rbnf_cur_token = None
                            lcl_7 = _rbnf_cur_token
                            rbnf_tmp_2 = lcl_7
                            lcl_7 = (rbnf_tmp_2 is None)
                            if lcl_7:
                                lcl_8 = builtin_tokens.offset
                                lcl_8 = (lcl_8, 'quote } not match')
                                lcl_8 = builtin_cons(lcl_8, builtin_nil)
                                lcl_8 = (False, lcl_8)
                                lcl_7 = lcl_8
                            else:
                                lcl_8 = Seq(rbnf_tmp_1)
                                lcl_8 = Block(lcl_8)
                                rbnf_tmp_1_ = lcl_8
                                lcl_8 = (True, rbnf_tmp_1_)
                                lcl_7 = lcl_8
                            lcl_6 = lcl_7
                        lcl_4 = lcl_6
                    elif (lcl_5 == 7):
                        lcl_6 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                        rbnf_named__check_1 = lcl_6
                        lcl_6 = rbnf_named__check_1[0]
                        lcl_6 = (lcl_6 == False)
                        if lcl_6:
                            lcl_6 = rbnf_named__check_1
                        else:
                            lcl_7 = rbnf_named__check_1[1]
                            rbnf_tmp_1 = lcl_7
                            try:
                                _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                if (_rbnf_cur_token.idint is 5):
                                    builtin_tokens.offset += 1
                                else:
                                    _rbnf_cur_token = None
                            except IndexError:
                                _rbnf_cur_token = None
                            lcl_7 = _rbnf_cur_token
                            rbnf_tmp_2 = lcl_7
                            lcl_7 = (rbnf_tmp_2 is None)
                            if lcl_7:
                                lcl_8 = builtin_tokens.offset
                                lcl_8 = (lcl_8, 'quote } not match')
                                lcl_8 = builtin_cons(lcl_8, builtin_nil)
                                lcl_8 = (False, lcl_8)
                                lcl_7 = lcl_8
                            else:
                                lcl_8 = Seq(rbnf_tmp_1)
                                lcl_8 = Block(lcl_8)
                                rbnf_tmp_1_ = lcl_8
                                lcl_8 = (True, rbnf_tmp_1_)
                                lcl_7 = lcl_8
                            lcl_6 = lcl_7
                        lcl_4 = lcl_6
                    elif (lcl_5 == 1):
                        lcl_6 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                        rbnf_named__check_1 = lcl_6
                        lcl_6 = rbnf_named__check_1[0]
                        lcl_6 = (lcl_6 == False)
                        if lcl_6:
                            lcl_6 = rbnf_named__check_1
                        else:
                            lcl_7 = rbnf_named__check_1[1]
                            rbnf_tmp_1 = lcl_7
                            try:
                                _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                if (_rbnf_cur_token.idint is 5):
                                    builtin_tokens.offset += 1
                                else:
                                    _rbnf_cur_token = None
                            except IndexError:
                                _rbnf_cur_token = None
                            lcl_7 = _rbnf_cur_token
                            rbnf_tmp_2 = lcl_7
                            lcl_7 = (rbnf_tmp_2 is None)
                            if lcl_7:
                                lcl_8 = builtin_tokens.offset
                                lcl_8 = (lcl_8, 'quote } not match')
                                lcl_8 = builtin_cons(lcl_8, builtin_nil)
                                lcl_8 = (False, lcl_8)
                                lcl_7 = lcl_8
                            else:
                                lcl_8 = Seq(rbnf_tmp_1)
                                lcl_8 = Block(lcl_8)
                                rbnf_tmp_1_ = lcl_8
                                lcl_8 = (True, rbnf_tmp_1_)
                                lcl_7 = lcl_8
                            lcl_6 = lcl_7
                        lcl_4 = lcl_6
                    elif (lcl_5 == 2):
                        lcl_6 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                        rbnf_named__check_1 = lcl_6
                        lcl_6 = rbnf_named__check_1[0]
                        lcl_6 = (lcl_6 == False)
                        if lcl_6:
                            lcl_6 = rbnf_named__check_1
                        else:
                            lcl_7 = rbnf_named__check_1[1]
                            rbnf_tmp_1 = lcl_7
                            try:
                                _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                if (_rbnf_cur_token.idint is 5):
                                    builtin_tokens.offset += 1
                                else:
                                    _rbnf_cur_token = None
                            except IndexError:
                                _rbnf_cur_token = None
                            lcl_7 = _rbnf_cur_token
                            rbnf_tmp_2 = lcl_7
                            lcl_7 = (rbnf_tmp_2 is None)
                            if lcl_7:
                                lcl_8 = builtin_tokens.offset
                                lcl_8 = (lcl_8, 'quote } not match')
                                lcl_8 = builtin_cons(lcl_8, builtin_nil)
                                lcl_8 = (False, lcl_8)
                                lcl_7 = lcl_8
                            else:
                                lcl_8 = Seq(rbnf_tmp_1)
                                lcl_8 = Block(lcl_8)
                                rbnf_tmp_1_ = lcl_8
                                lcl_8 = (True, rbnf_tmp_1_)
                                lcl_7 = lcl_8
                            lcl_6 = lcl_7
                        lcl_4 = lcl_6
                    else:
                        lcl_6 = (rbnf_named__off_1, 'Atom lookahead failed')
                        lcl_6 = builtin_cons(lcl_6, builtin_nil)
                        lcl_6 = (False, lcl_6)
                        lcl_4 = lcl_6
                    lcl_3 = lcl_4
                else:
                    lcl_4 = (rbnf_named__off_1, 'Atom got EOF')
                    lcl_4 = builtin_cons(lcl_4, builtin_nil)
                    lcl_4 = (False, lcl_4)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 0):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = builtin_tokens.offset
                rbnf_named__off_1 = lcl_3
                try:
                    builtin_tokens.array[(builtin_tokens.offset + 0)]
                    _rbnf_peek_tmp = True
                except IndexError:
                    _rbnf_peek_tmp = False
                lcl_3 = _rbnf_peek_tmp
                if lcl_3:
                    lcl_5 = builtin_tokens.array[(builtin_tokens.offset + 0)]
                    lcl_5 = lcl_5.idint
                    if (lcl_5 == 5):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        lcl_6 = rbnf_tmp_1.value
                        lcl_6 = control(lcl_6)
                        rbnf_tmp_1_ = lcl_6
                        lcl_6 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_6
                    elif (lcl_5 == 4):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        lcl_6 = rbnf_tmp_1.value
                        lcl_6 = control(lcl_6)
                        rbnf_tmp_1_ = lcl_6
                        lcl_6 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_6
                    elif (lcl_5 == 6):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        lcl_6 = rbnf_tmp_1.value
                        lcl_6 = control(lcl_6)
                        rbnf_tmp_1_ = lcl_6
                        lcl_6 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_6
                    elif (lcl_5 == 0):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        lcl_6 = rbnf_tmp_1.value
                        lcl_6 = control(lcl_6)
                        rbnf_tmp_1_ = lcl_6
                        lcl_6 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_6
                    elif (lcl_5 == 3):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        lcl_6 = rbnf_tmp_1.value
                        lcl_6 = control(lcl_6)
                        rbnf_tmp_1_ = lcl_6
                        lcl_6 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_6
                    elif (lcl_5 == 7):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        lcl_6 = rbnf_tmp_1.value
                        lcl_6 = control(lcl_6)
                        rbnf_tmp_1_ = lcl_6
                        lcl_6 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_6
                    elif (lcl_5 == 1):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        lcl_6 = rbnf_tmp_1.value
                        lcl_6 = control(lcl_6)
                        rbnf_tmp_1_ = lcl_6
                        lcl_6 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_6
                    elif (lcl_5 == 2):
                        lcl_6 = rbnf_named_parse_Command(builtin_state, builtin_tokens)
                        rbnf_named__check_1 = lcl_6
                        lcl_6 = rbnf_named__check_1[0]
                        lcl_6 = (lcl_6 == False)
                        if lcl_6:
                            lcl_6 = rbnf_named__check_1
                        else:
                            lcl_7 = rbnf_named__check_1[1]
                            rbnf_tmp_1 = lcl_7
                            rbnf_tmp_1_ = rbnf_tmp_1
                            lcl_7 = (True, rbnf_tmp_1_)
                            lcl_6 = lcl_7
                        lcl_4 = lcl_6
                    else:
                        lcl_6 = (rbnf_named__off_1, 'Atom lookahead failed')
                        lcl_6 = builtin_cons(lcl_6, builtin_nil)
                        lcl_6 = (False, lcl_6)
                        lcl_4 = lcl_6
                    lcl_3 = lcl_4
                else:
                    lcl_4 = (rbnf_named__off_1, 'Atom got EOF')
                    lcl_4 = builtin_cons(lcl_4, builtin_nil)
                    lcl_4 = (False, lcl_4)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 3):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = rbnf_named_parse_Arg(builtin_state, builtin_tokens)
                rbnf_named__check_1 = lcl_3
                lcl_3 = rbnf_named__check_1[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_1
                else:
                    lcl_4 = rbnf_named__check_1[1]
                    rbnf_tmp_1 = lcl_4
                    lcl_4 = mkArg(rbnf_tmp_1)
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = (True, rbnf_tmp_1_)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 7):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = rbnf_tmp_0.value
                lcl_3 = Text(lcl_3)
                rbnf_tmp_1_ = lcl_3
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            elif (lcl_2 == 1):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = rbnf_tmp_0.value
                lcl_3 = Text(lcl_3)
                rbnf_tmp_1_ = lcl_3
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            elif (lcl_2 == 2):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = rbnf_tmp_0.value
                lcl_3 = Text(lcl_3)
                rbnf_tmp_1_ = lcl_3
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            else:
                lcl_3 = (rbnf_named__off_0, 'Atom lookahead failed')
                lcl_3 = builtin_cons(lcl_3, builtin_nil)
                lcl_3 = (False, lcl_3)
                lcl_1 = lcl_3
            lcl_0 = lcl_1
        else:
            lcl_1 = (rbnf_named__off_0, 'Atom got EOF')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_Command(builtin_state, builtin_tokens):
        try:
            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
            if (_rbnf_cur_token.idint is 2):
                builtin_tokens.offset += 1
            else:
                _rbnf_cur_token = None
        except IndexError:
            _rbnf_cur_token = None
        lcl_0 = _rbnf_cur_token
        rbnf_tmp_0 = lcl_0
        lcl_0 = (rbnf_tmp_0 is None)
        if lcl_0:
            lcl_1 = builtin_tokens.offset
            lcl_1 = (lcl_1, 'Id not match')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        else:
            lcl_1 = builtin_tokens.offset
            rbnf_named__off_1 = lcl_1
            try:
                builtin_tokens.array[(builtin_tokens.offset + 0)]
                _rbnf_peek_tmp = True
            except IndexError:
                _rbnf_peek_tmp = False
            lcl_1 = _rbnf_peek_tmp
            if lcl_1:
                lcl_3 = builtin_tokens.array[(builtin_tokens.offset + 0)]
                lcl_3 = lcl_3.idint
                if (lcl_3 == 4):
                    lcl_4 = rbnf_named_parse_Groups(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_4
                    lcl_4 = rbnf_named__check_1[0]
                    lcl_4 = (lcl_4 == False)
                    if lcl_4:
                        lcl_4 = rbnf_named__check_1
                    else:
                        lcl_5 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_5
                        lcl_5 = rbnf_tmp_0.value
                        lcl_5 = Command(lcl_5, rbnf_tmp_1)
                        rbnf_tmp_1_ = lcl_5
                        lcl_5 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_5
                    lcl_2 = lcl_4
                else:
                    lcl_4 = rbnf_tmp_0.value
                    lcl_4 = Command(lcl_4, None)
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = (True, rbnf_tmp_1_)
                    lcl_2 = lcl_4
                lcl_1 = lcl_2
            else:
                lcl_2 = (rbnf_named__off_1, 'Command got EOF')
                lcl_2 = builtin_cons(lcl_2, builtin_nil)
                lcl_2 = (False, lcl_2)
                lcl_1 = lcl_2
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_Group(builtin_state, builtin_tokens):
        try:
            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
            if (_rbnf_cur_token.idint is 4):
                builtin_tokens.offset += 1
            else:
                _rbnf_cur_token = None
        except IndexError:
            _rbnf_cur_token = None
        lcl_0 = _rbnf_cur_token
        rbnf_tmp_0 = lcl_0
        lcl_0 = (rbnf_tmp_0 is None)
        if lcl_0:
            lcl_1 = builtin_tokens.offset
            lcl_1 = (lcl_1, 'quote { not match')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        else:
            lcl_1 = builtin_tokens.offset
            rbnf_named__off_1 = lcl_1
            try:
                builtin_tokens.array[(builtin_tokens.offset + 0)]
                _rbnf_peek_tmp = True
            except IndexError:
                _rbnf_peek_tmp = False
            lcl_1 = _rbnf_peek_tmp
            if lcl_1:
                lcl_3 = builtin_tokens.array[(builtin_tokens.offset + 0)]
                lcl_3 = lcl_3.idint
                if (lcl_3 == 5):
                    _rbnf_old_offset = builtin_tokens.offset
                    _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                    builtin_tokens.offset = (_rbnf_old_offset + 1)
                    lcl_4 = _rbnf_cur_token
                    rbnf_tmp_1 = lcl_4
                    lcl_4 = rbnf_tmp_0.offset
                    lcl_4 = add1(lcl_4)
                    lcl_5 = rbnf_tmp_1.offset
                    lcl_4 = PosGroup(lcl_4, None, lcl_5)
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = (True, rbnf_tmp_1_)
                    lcl_2 = lcl_4
                elif (lcl_3 == 4):
                    lcl_4 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_4
                    lcl_4 = rbnf_named__check_1[0]
                    lcl_4 = (lcl_4 == False)
                    if lcl_4:
                        lcl_4 = rbnf_named__check_1
                    else:
                        lcl_5 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_5
                        try:
                            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                            if (_rbnf_cur_token.idint is 5):
                                builtin_tokens.offset += 1
                            else:
                                _rbnf_cur_token = None
                        except IndexError:
                            _rbnf_cur_token = None
                        lcl_5 = _rbnf_cur_token
                        rbnf_tmp_2 = lcl_5
                        lcl_5 = (rbnf_tmp_2 is None)
                        if lcl_5:
                            lcl_6 = builtin_tokens.offset
                            lcl_6 = (lcl_6, 'quote } not match')
                            lcl_6 = builtin_cons(lcl_6, builtin_nil)
                            lcl_6 = (False, lcl_6)
                            lcl_5 = lcl_6
                        else:
                            lcl_6 = rbnf_tmp_0.offset
                            lcl_6 = add1(lcl_6)
                            lcl_7 = Seq(rbnf_tmp_1)
                            lcl_8 = rbnf_tmp_2.offset
                            lcl_6 = PosGroup(lcl_6, lcl_7, lcl_8)
                            rbnf_tmp_1_ = lcl_6
                            lcl_6 = (True, rbnf_tmp_1_)
                            lcl_5 = lcl_6
                        lcl_4 = lcl_5
                    lcl_2 = lcl_4
                elif (lcl_3 == 6):
                    _rbnf_old_offset = builtin_tokens.offset
                    _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                    builtin_tokens.offset = (_rbnf_old_offset + 1)
                    lcl_4 = _rbnf_cur_token
                    rbnf_tmp_1 = lcl_4
                    try:
                        _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                        if (_rbnf_cur_token.idint is 2):
                            builtin_tokens.offset += 1
                        else:
                            _rbnf_cur_token = None
                    except IndexError:
                        _rbnf_cur_token = None
                    lcl_4 = _rbnf_cur_token
                    rbnf_tmp_2 = lcl_4
                    lcl_4 = (rbnf_tmp_2 is None)
                    if lcl_4:
                        lcl_5 = builtin_tokens.offset
                        lcl_5 = (lcl_5, 'Id not match')
                        lcl_5 = builtin_cons(lcl_5, builtin_nil)
                        lcl_5 = (False, lcl_5)
                        lcl_4 = lcl_5
                    else:
                        lcl_5 = builtin_tokens.offset
                        rbnf_named__off_3 = lcl_5
                        try:
                            builtin_tokens.array[(builtin_tokens.offset + 0)]
                            _rbnf_peek_tmp = True
                        except IndexError:
                            _rbnf_peek_tmp = False
                        lcl_5 = _rbnf_peek_tmp
                        if lcl_5:
                            lcl_7 = builtin_tokens.array[(builtin_tokens.offset + 0)]
                            lcl_7 = lcl_7.idint
                            if (lcl_7 == 5):
                                _rbnf_old_offset = builtin_tokens.offset
                                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                                builtin_tokens.offset = (_rbnf_old_offset + 1)
                                lcl_8 = _rbnf_cur_token
                                rbnf_tmp_3 = lcl_8
                                lcl_8 = rbnf_tmp_0.offset
                                lcl_8 = add1(lcl_8)
                                lcl_9 = rbnf_tmp_2.value
                                lcl_10 = rbnf_tmp_3.offset
                                lcl_10 = KwGroup(lcl_8, lcl_9, None, lcl_10)
                                rbnf_tmp_1_ = lcl_10
                                lcl_10 = (True, rbnf_tmp_1_)
                                lcl_6 = lcl_10
                            elif (lcl_7 == 4):
                                lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                                rbnf_named__check_3 = lcl_10
                                lcl_10 = rbnf_named__check_3[0]
                                lcl_10 = (lcl_10 == False)
                                if lcl_10:
                                    lcl_10 = rbnf_named__check_3
                                else:
                                    lcl_8 = rbnf_named__check_3[1]
                                    rbnf_tmp_3 = lcl_8
                                    try:
                                        _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                        if (_rbnf_cur_token.idint is 5):
                                            builtin_tokens.offset += 1
                                        else:
                                            _rbnf_cur_token = None
                                    except IndexError:
                                        _rbnf_cur_token = None
                                    lcl_8 = _rbnf_cur_token
                                    rbnf_tmp_4 = lcl_8
                                    lcl_8 = (rbnf_tmp_4 is None)
                                    if lcl_8:
                                        lcl_9 = builtin_tokens.offset
                                        lcl_9 = (lcl_9, 'quote } not match')
                                        lcl_9 = builtin_cons(lcl_9, builtin_nil)
                                        lcl_9 = (False, lcl_9)
                                        lcl_8 = lcl_9
                                    else:
                                        lcl_9 = rbnf_tmp_0.offset
                                        lcl_9 = add1(lcl_9)
                                        lcl_11 = rbnf_tmp_2.value
                                        lcl_12 = Seq(rbnf_tmp_3)
                                        lcl_13 = rbnf_tmp_4.offset
                                        lcl_11 = KwGroup(lcl_9, lcl_11, lcl_12, lcl_13)
                                        rbnf_tmp_1_ = lcl_11
                                        lcl_11 = (True, rbnf_tmp_1_)
                                        lcl_8 = lcl_11
                                    lcl_10 = lcl_8
                                lcl_6 = lcl_10
                            elif (lcl_7 == 0):
                                lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                                rbnf_named__check_3 = lcl_10
                                lcl_10 = rbnf_named__check_3[0]
                                lcl_10 = (lcl_10 == False)
                                if lcl_10:
                                    lcl_10 = rbnf_named__check_3
                                else:
                                    lcl_11 = rbnf_named__check_3[1]
                                    rbnf_tmp_3 = lcl_11
                                    try:
                                        _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                        if (_rbnf_cur_token.idint is 5):
                                            builtin_tokens.offset += 1
                                        else:
                                            _rbnf_cur_token = None
                                    except IndexError:
                                        _rbnf_cur_token = None
                                    lcl_11 = _rbnf_cur_token
                                    rbnf_tmp_4 = lcl_11
                                    lcl_11 = (rbnf_tmp_4 is None)
                                    if lcl_11:
                                        lcl_12 = builtin_tokens.offset
                                        lcl_12 = (lcl_12, 'quote } not match')
                                        lcl_12 = builtin_cons(lcl_12, builtin_nil)
                                        lcl_12 = (False, lcl_12)
                                        lcl_11 = lcl_12
                                    else:
                                        lcl_12 = rbnf_tmp_0.offset
                                        lcl_12 = add1(lcl_12)
                                        lcl_13 = rbnf_tmp_2.value
                                        lcl_8 = Seq(rbnf_tmp_3)
                                        lcl_9 = rbnf_tmp_4.offset
                                        lcl_12 = KwGroup(lcl_12, lcl_13, lcl_8, lcl_9)
                                        rbnf_tmp_1_ = lcl_12
                                        lcl_12 = (True, rbnf_tmp_1_)
                                        lcl_11 = lcl_12
                                    lcl_10 = lcl_11
                                lcl_6 = lcl_10
                            elif (lcl_7 == 3):
                                lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                                rbnf_named__check_3 = lcl_10
                                lcl_10 = rbnf_named__check_3[0]
                                lcl_10 = (lcl_10 == False)
                                if lcl_10:
                                    lcl_10 = rbnf_named__check_3
                                else:
                                    lcl_11 = rbnf_named__check_3[1]
                                    rbnf_tmp_3 = lcl_11
                                    try:
                                        _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                        if (_rbnf_cur_token.idint is 5):
                                            builtin_tokens.offset += 1
                                        else:
                                            _rbnf_cur_token = None
                                    except IndexError:
                                        _rbnf_cur_token = None
                                    lcl_11 = _rbnf_cur_token
                                    rbnf_tmp_4 = lcl_11
                                    lcl_11 = (rbnf_tmp_4 is None)
                                    if lcl_11:
                                        lcl_12 = builtin_tokens.offset
                                        lcl_12 = (lcl_12, 'quote } not match')
                                        lcl_12 = builtin_cons(lcl_12, builtin_nil)
                                        lcl_12 = (False, lcl_12)
                                        lcl_11 = lcl_12
                                    else:
                                        lcl_12 = rbnf_tmp_0.offset
                                        lcl_12 = add1(lcl_12)
                                        lcl_13 = rbnf_tmp_2.value
                                        lcl_8 = Seq(rbnf_tmp_3)
                                        lcl_9 = rbnf_tmp_4.offset
                                        lcl_12 = KwGroup(lcl_12, lcl_13, lcl_8, lcl_9)
                                        rbnf_tmp_1_ = lcl_12
                                        lcl_12 = (True, rbnf_tmp_1_)
                                        lcl_11 = lcl_12
                                    lcl_10 = lcl_11
                                lcl_6 = lcl_10
                            elif (lcl_7 == 9):
                                lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                                rbnf_named__check_3 = lcl_10
                                lcl_10 = rbnf_named__check_3[0]
                                lcl_10 = (lcl_10 == False)
                                if lcl_10:
                                    lcl_10 = rbnf_named__check_3
                                else:
                                    lcl_11 = rbnf_named__check_3[1]
                                    rbnf_tmp_3 = lcl_11
                                    try:
                                        _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                        if (_rbnf_cur_token.idint is 5):
                                            builtin_tokens.offset += 1
                                        else:
                                            _rbnf_cur_token = None
                                    except IndexError:
                                        _rbnf_cur_token = None
                                    lcl_11 = _rbnf_cur_token
                                    rbnf_tmp_4 = lcl_11
                                    lcl_11 = (rbnf_tmp_4 is None)
                                    if lcl_11:
                                        lcl_12 = builtin_tokens.offset
                                        lcl_12 = (lcl_12, 'quote } not match')
                                        lcl_12 = builtin_cons(lcl_12, builtin_nil)
                                        lcl_12 = (False, lcl_12)
                                        lcl_11 = lcl_12
                                    else:
                                        lcl_12 = rbnf_tmp_0.offset
                                        lcl_12 = add1(lcl_12)
                                        lcl_13 = rbnf_tmp_2.value
                                        lcl_8 = Seq(rbnf_tmp_3)
                                        lcl_9 = rbnf_tmp_4.offset
                                        lcl_12 = KwGroup(lcl_12, lcl_13, lcl_8, lcl_9)
                                        rbnf_tmp_1_ = lcl_12
                                        lcl_12 = (True, rbnf_tmp_1_)
                                        lcl_11 = lcl_12
                                    lcl_10 = lcl_11
                                lcl_6 = lcl_10
                            elif (lcl_7 == 7):
                                lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                                rbnf_named__check_3 = lcl_10
                                lcl_10 = rbnf_named__check_3[0]
                                lcl_10 = (lcl_10 == False)
                                if lcl_10:
                                    lcl_10 = rbnf_named__check_3
                                else:
                                    lcl_11 = rbnf_named__check_3[1]
                                    rbnf_tmp_3 = lcl_11
                                    try:
                                        _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                        if (_rbnf_cur_token.idint is 5):
                                            builtin_tokens.offset += 1
                                        else:
                                            _rbnf_cur_token = None
                                    except IndexError:
                                        _rbnf_cur_token = None
                                    lcl_11 = _rbnf_cur_token
                                    rbnf_tmp_4 = lcl_11
                                    lcl_11 = (rbnf_tmp_4 is None)
                                    if lcl_11:
                                        lcl_12 = builtin_tokens.offset
                                        lcl_12 = (lcl_12, 'quote } not match')
                                        lcl_12 = builtin_cons(lcl_12, builtin_nil)
                                        lcl_12 = (False, lcl_12)
                                        lcl_11 = lcl_12
                                    else:
                                        lcl_12 = rbnf_tmp_0.offset
                                        lcl_12 = add1(lcl_12)
                                        lcl_13 = rbnf_tmp_2.value
                                        lcl_8 = Seq(rbnf_tmp_3)
                                        lcl_9 = rbnf_tmp_4.offset
                                        lcl_12 = KwGroup(lcl_12, lcl_13, lcl_8, lcl_9)
                                        rbnf_tmp_1_ = lcl_12
                                        lcl_12 = (True, rbnf_tmp_1_)
                                        lcl_11 = lcl_12
                                    lcl_10 = lcl_11
                                lcl_6 = lcl_10
                            elif (lcl_7 == 1):
                                lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                                rbnf_named__check_3 = lcl_10
                                lcl_10 = rbnf_named__check_3[0]
                                lcl_10 = (lcl_10 == False)
                                if lcl_10:
                                    lcl_10 = rbnf_named__check_3
                                else:
                                    lcl_11 = rbnf_named__check_3[1]
                                    rbnf_tmp_3 = lcl_11
                                    try:
                                        _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                        if (_rbnf_cur_token.idint is 5):
                                            builtin_tokens.offset += 1
                                        else:
                                            _rbnf_cur_token = None
                                    except IndexError:
                                        _rbnf_cur_token = None
                                    lcl_11 = _rbnf_cur_token
                                    rbnf_tmp_4 = lcl_11
                                    lcl_11 = (rbnf_tmp_4 is None)
                                    if lcl_11:
                                        lcl_12 = builtin_tokens.offset
                                        lcl_12 = (lcl_12, 'quote } not match')
                                        lcl_12 = builtin_cons(lcl_12, builtin_nil)
                                        lcl_12 = (False, lcl_12)
                                        lcl_11 = lcl_12
                                    else:
                                        lcl_12 = rbnf_tmp_0.offset
                                        lcl_12 = add1(lcl_12)
                                        lcl_13 = rbnf_tmp_2.value
                                        lcl_8 = Seq(rbnf_tmp_3)
                                        lcl_9 = rbnf_tmp_4.offset
                                        lcl_12 = KwGroup(lcl_12, lcl_13, lcl_8, lcl_9)
                                        rbnf_tmp_1_ = lcl_12
                                        lcl_12 = (True, rbnf_tmp_1_)
                                        lcl_11 = lcl_12
                                    lcl_10 = lcl_11
                                lcl_6 = lcl_10
                            elif (lcl_7 == 2):
                                lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                                rbnf_named__check_3 = lcl_10
                                lcl_10 = rbnf_named__check_3[0]
                                lcl_10 = (lcl_10 == False)
                                if lcl_10:
                                    lcl_10 = rbnf_named__check_3
                                else:
                                    lcl_11 = rbnf_named__check_3[1]
                                    rbnf_tmp_3 = lcl_11
                                    try:
                                        _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                                        if (_rbnf_cur_token.idint is 5):
                                            builtin_tokens.offset += 1
                                        else:
                                            _rbnf_cur_token = None
                                    except IndexError:
                                        _rbnf_cur_token = None
                                    lcl_11 = _rbnf_cur_token
                                    rbnf_tmp_4 = lcl_11
                                    lcl_11 = (rbnf_tmp_4 is None)
                                    if lcl_11:
                                        lcl_12 = builtin_tokens.offset
                                        lcl_12 = (lcl_12, 'quote } not match')
                                        lcl_12 = builtin_cons(lcl_12, builtin_nil)
                                        lcl_12 = (False, lcl_12)
                                        lcl_11 = lcl_12
                                    else:
                                        lcl_12 = rbnf_tmp_0.offset
                                        lcl_12 = add1(lcl_12)
                                        lcl_13 = rbnf_tmp_2.value
                                        lcl_8 = Seq(rbnf_tmp_3)
                                        lcl_9 = rbnf_tmp_4.offset
                                        lcl_12 = KwGroup(lcl_12, lcl_13, lcl_8, lcl_9)
                                        rbnf_tmp_1_ = lcl_12
                                        lcl_12 = (True, rbnf_tmp_1_)
                                        lcl_11 = lcl_12
                                    lcl_10 = lcl_11
                                lcl_6 = lcl_10
                            else:
                                lcl_10 = (rbnf_named__off_3, 'Group lookahead failed')
                                lcl_10 = builtin_cons(lcl_10, builtin_nil)
                                lcl_10 = (False, lcl_10)
                                lcl_6 = lcl_10
                            lcl_5 = lcl_6
                        else:
                            lcl_10 = (rbnf_named__off_3, 'Group got EOF')
                            lcl_10 = builtin_cons(lcl_10, builtin_nil)
                            lcl_10 = (False, lcl_10)
                            lcl_5 = lcl_10
                        lcl_4 = lcl_5
                    lcl_2 = lcl_4
                elif (lcl_3 == 0):
                    lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_10
                    lcl_10 = rbnf_named__check_1[0]
                    lcl_10 = (lcl_10 == False)
                    if lcl_10:
                        lcl_10 = rbnf_named__check_1
                    else:
                        lcl_11 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_11
                        try:
                            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                            if (_rbnf_cur_token.idint is 5):
                                builtin_tokens.offset += 1
                            else:
                                _rbnf_cur_token = None
                        except IndexError:
                            _rbnf_cur_token = None
                        lcl_11 = _rbnf_cur_token
                        rbnf_tmp_2 = lcl_11
                        lcl_11 = (rbnf_tmp_2 is None)
                        if lcl_11:
                            lcl_12 = builtin_tokens.offset
                            lcl_12 = (lcl_12, 'quote } not match')
                            lcl_12 = builtin_cons(lcl_12, builtin_nil)
                            lcl_12 = (False, lcl_12)
                            lcl_11 = lcl_12
                        else:
                            lcl_12 = rbnf_tmp_0.offset
                            lcl_12 = add1(lcl_12)
                            lcl_13 = Seq(rbnf_tmp_1)
                            lcl_4 = rbnf_tmp_2.offset
                            lcl_12 = PosGroup(lcl_12, lcl_13, lcl_4)
                            rbnf_tmp_1_ = lcl_12
                            lcl_12 = (True, rbnf_tmp_1_)
                            lcl_11 = lcl_12
                        lcl_10 = lcl_11
                    lcl_2 = lcl_10
                elif (lcl_3 == 3):
                    lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_10
                    lcl_10 = rbnf_named__check_1[0]
                    lcl_10 = (lcl_10 == False)
                    if lcl_10:
                        lcl_10 = rbnf_named__check_1
                    else:
                        lcl_11 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_11
                        try:
                            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                            if (_rbnf_cur_token.idint is 5):
                                builtin_tokens.offset += 1
                            else:
                                _rbnf_cur_token = None
                        except IndexError:
                            _rbnf_cur_token = None
                        lcl_11 = _rbnf_cur_token
                        rbnf_tmp_2 = lcl_11
                        lcl_11 = (rbnf_tmp_2 is None)
                        if lcl_11:
                            lcl_12 = builtin_tokens.offset
                            lcl_12 = (lcl_12, 'quote } not match')
                            lcl_12 = builtin_cons(lcl_12, builtin_nil)
                            lcl_12 = (False, lcl_12)
                            lcl_11 = lcl_12
                        else:
                            lcl_12 = rbnf_tmp_0.offset
                            lcl_12 = add1(lcl_12)
                            lcl_13 = Seq(rbnf_tmp_1)
                            lcl_4 = rbnf_tmp_2.offset
                            lcl_12 = PosGroup(lcl_12, lcl_13, lcl_4)
                            rbnf_tmp_1_ = lcl_12
                            lcl_12 = (True, rbnf_tmp_1_)
                            lcl_11 = lcl_12
                        lcl_10 = lcl_11
                    lcl_2 = lcl_10
                elif (lcl_3 == 9):
                    lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_10
                    lcl_10 = rbnf_named__check_1[0]
                    lcl_10 = (lcl_10 == False)
                    if lcl_10:
                        lcl_10 = rbnf_named__check_1
                    else:
                        lcl_11 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_11
                        try:
                            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                            if (_rbnf_cur_token.idint is 5):
                                builtin_tokens.offset += 1
                            else:
                                _rbnf_cur_token = None
                        except IndexError:
                            _rbnf_cur_token = None
                        lcl_11 = _rbnf_cur_token
                        rbnf_tmp_2 = lcl_11
                        lcl_11 = (rbnf_tmp_2 is None)
                        if lcl_11:
                            lcl_12 = builtin_tokens.offset
                            lcl_12 = (lcl_12, 'quote } not match')
                            lcl_12 = builtin_cons(lcl_12, builtin_nil)
                            lcl_12 = (False, lcl_12)
                            lcl_11 = lcl_12
                        else:
                            lcl_12 = rbnf_tmp_0.offset
                            lcl_12 = add1(lcl_12)
                            lcl_13 = Seq(rbnf_tmp_1)
                            lcl_4 = rbnf_tmp_2.offset
                            lcl_12 = PosGroup(lcl_12, lcl_13, lcl_4)
                            rbnf_tmp_1_ = lcl_12
                            lcl_12 = (True, rbnf_tmp_1_)
                            lcl_11 = lcl_12
                        lcl_10 = lcl_11
                    lcl_2 = lcl_10
                elif (lcl_3 == 7):
                    lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_10
                    lcl_10 = rbnf_named__check_1[0]
                    lcl_10 = (lcl_10 == False)
                    if lcl_10:
                        lcl_10 = rbnf_named__check_1
                    else:
                        lcl_11 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_11
                        try:
                            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                            if (_rbnf_cur_token.idint is 5):
                                builtin_tokens.offset += 1
                            else:
                                _rbnf_cur_token = None
                        except IndexError:
                            _rbnf_cur_token = None
                        lcl_11 = _rbnf_cur_token
                        rbnf_tmp_2 = lcl_11
                        lcl_11 = (rbnf_tmp_2 is None)
                        if lcl_11:
                            lcl_12 = builtin_tokens.offset
                            lcl_12 = (lcl_12, 'quote } not match')
                            lcl_12 = builtin_cons(lcl_12, builtin_nil)
                            lcl_12 = (False, lcl_12)
                            lcl_11 = lcl_12
                        else:
                            lcl_12 = rbnf_tmp_0.offset
                            lcl_12 = add1(lcl_12)
                            lcl_13 = Seq(rbnf_tmp_1)
                            lcl_4 = rbnf_tmp_2.offset
                            lcl_12 = PosGroup(lcl_12, lcl_13, lcl_4)
                            rbnf_tmp_1_ = lcl_12
                            lcl_12 = (True, rbnf_tmp_1_)
                            lcl_11 = lcl_12
                        lcl_10 = lcl_11
                    lcl_2 = lcl_10
                elif (lcl_3 == 1):
                    lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_10
                    lcl_10 = rbnf_named__check_1[0]
                    lcl_10 = (lcl_10 == False)
                    if lcl_10:
                        lcl_10 = rbnf_named__check_1
                    else:
                        lcl_11 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_11
                        try:
                            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                            if (_rbnf_cur_token.idint is 5):
                                builtin_tokens.offset += 1
                            else:
                                _rbnf_cur_token = None
                        except IndexError:
                            _rbnf_cur_token = None
                        lcl_11 = _rbnf_cur_token
                        rbnf_tmp_2 = lcl_11
                        lcl_11 = (rbnf_tmp_2 is None)
                        if lcl_11:
                            lcl_12 = builtin_tokens.offset
                            lcl_12 = (lcl_12, 'quote } not match')
                            lcl_12 = builtin_cons(lcl_12, builtin_nil)
                            lcl_12 = (False, lcl_12)
                            lcl_11 = lcl_12
                        else:
                            lcl_12 = rbnf_tmp_0.offset
                            lcl_12 = add1(lcl_12)
                            lcl_13 = Seq(rbnf_tmp_1)
                            lcl_4 = rbnf_tmp_2.offset
                            lcl_12 = PosGroup(lcl_12, lcl_13, lcl_4)
                            rbnf_tmp_1_ = lcl_12
                            lcl_12 = (True, rbnf_tmp_1_)
                            lcl_11 = lcl_12
                        lcl_10 = lcl_11
                    lcl_2 = lcl_10
                elif (lcl_3 == 2):
                    lcl_10 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_10
                    lcl_10 = rbnf_named__check_1[0]
                    lcl_10 = (lcl_10 == False)
                    if lcl_10:
                        lcl_10 = rbnf_named__check_1
                    else:
                        lcl_11 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_11
                        try:
                            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                            if (_rbnf_cur_token.idint is 5):
                                builtin_tokens.offset += 1
                            else:
                                _rbnf_cur_token = None
                        except IndexError:
                            _rbnf_cur_token = None
                        lcl_11 = _rbnf_cur_token
                        rbnf_tmp_2 = lcl_11
                        lcl_11 = (rbnf_tmp_2 is None)
                        if lcl_11:
                            lcl_12 = builtin_tokens.offset
                            lcl_12 = (lcl_12, 'quote } not match')
                            lcl_12 = builtin_cons(lcl_12, builtin_nil)
                            lcl_12 = (False, lcl_12)
                            lcl_11 = lcl_12
                        else:
                            lcl_12 = rbnf_tmp_0.offset
                            lcl_12 = add1(lcl_12)
                            lcl_13 = Seq(rbnf_tmp_1)
                            lcl_4 = rbnf_tmp_2.offset
                            lcl_12 = PosGroup(lcl_12, lcl_13, lcl_4)
                            rbnf_tmp_1_ = lcl_12
                            lcl_12 = (True, rbnf_tmp_1_)
                            lcl_11 = lcl_12
                        lcl_10 = lcl_11
                    lcl_2 = lcl_10
                else:
                    lcl_10 = (rbnf_named__off_1, 'Group lookahead failed')
                    lcl_10 = builtin_cons(lcl_10, builtin_nil)
                    lcl_10 = (False, lcl_10)
                    lcl_2 = lcl_10
                lcl_1 = lcl_2
            else:
                lcl_10 = (rbnf_named__off_1, 'Group got EOF')
                lcl_10 = builtin_cons(lcl_10, builtin_nil)
                lcl_10 = (False, lcl_10)
                lcl_1 = lcl_10
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_Groups(builtin_state, builtin_tokens):
        lcl_0 = rbnf_named_parse_Group(builtin_state, builtin_tokens)
        rbnf_named__check_0 = lcl_0
        lcl_0 = rbnf_named__check_0[0]
        lcl_0 = (lcl_0 == False)
        if lcl_0:
            lcl_0 = rbnf_named__check_0
        else:
            lcl_1 = rbnf_named__check_0[1]
            rbnf_tmp_0 = lcl_1
            lcl_1 = []
            _rbnf_immediate_lst = lcl_1
            _rbnf_immediate_lst.append(rbnf_tmp_0)
            lcl_1 = _rbnf_immediate_lst
            rbnf_tmp_1_ = lcl_1
            lcl_1 = rbnf_named_lr_loop_Groups(rbnf_tmp_1_, builtin_state, builtin_tokens)
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_Objects(builtin_state, builtin_tokens):
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        try:
            builtin_tokens.array[(builtin_tokens.offset + 0)]
            _rbnf_peek_tmp = True
        except IndexError:
            _rbnf_peek_tmp = False
        lcl_0 = _rbnf_peek_tmp
        if lcl_0:
            lcl_2 = builtin_tokens.array[(builtin_tokens.offset + 0)]
            lcl_2 = lcl_2.idint
            if (lcl_2 == 4):
                lcl_3 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_0 = lcl_3
                lcl_3 = rbnf_named__check_0[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_0
                else:
                    lcl_4 = rbnf_named__check_0[1]
                    rbnf_tmp_0 = lcl_4
                    lcl_4 = []
                    _rbnf_immediate_lst = lcl_4
                    _rbnf_immediate_lst.append(rbnf_tmp_0)
                    lcl_4 = _rbnf_immediate_lst
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = rbnf_named_lr_loop_Objects(rbnf_tmp_1_, builtin_state, builtin_tokens)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 0):
                lcl_3 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_0 = lcl_3
                lcl_3 = rbnf_named__check_0[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_0
                else:
                    lcl_4 = rbnf_named__check_0[1]
                    rbnf_tmp_0 = lcl_4
                    lcl_4 = []
                    _rbnf_immediate_lst = lcl_4
                    _rbnf_immediate_lst.append(rbnf_tmp_0)
                    lcl_4 = _rbnf_immediate_lst
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = rbnf_named_lr_loop_Objects(rbnf_tmp_1_, builtin_state, builtin_tokens)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 3):
                lcl_3 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_0 = lcl_3
                lcl_3 = rbnf_named__check_0[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_0
                else:
                    lcl_4 = rbnf_named__check_0[1]
                    rbnf_tmp_0 = lcl_4
                    lcl_4 = []
                    _rbnf_immediate_lst = lcl_4
                    _rbnf_immediate_lst.append(rbnf_tmp_0)
                    lcl_4 = _rbnf_immediate_lst
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = rbnf_named_lr_loop_Objects(rbnf_tmp_1_, builtin_state, builtin_tokens)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 9):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = []
                lcl_4 = rbnf_tmp_0.value
                lcl_4 = Whitespace(lcl_4)
                _rbnf_immediate_lst = lcl_3
                _rbnf_immediate_lst.append(lcl_4)
                lcl_3 = _rbnf_immediate_lst
                rbnf_tmp_1_ = lcl_3
                lcl_3 = rbnf_named_lr_loop_Objects(rbnf_tmp_1_, builtin_state, builtin_tokens)
                lcl_1 = lcl_3
            elif (lcl_2 == 7):
                lcl_3 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_0 = lcl_3
                lcl_3 = rbnf_named__check_0[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_0
                else:
                    lcl_4 = rbnf_named__check_0[1]
                    rbnf_tmp_0 = lcl_4
                    lcl_4 = []
                    _rbnf_immediate_lst = lcl_4
                    _rbnf_immediate_lst.append(rbnf_tmp_0)
                    lcl_4 = _rbnf_immediate_lst
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = rbnf_named_lr_loop_Objects(rbnf_tmp_1_, builtin_state, builtin_tokens)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 1):
                lcl_3 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_0 = lcl_3
                lcl_3 = rbnf_named__check_0[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_0
                else:
                    lcl_4 = rbnf_named__check_0[1]
                    rbnf_tmp_0 = lcl_4
                    lcl_4 = []
                    _rbnf_immediate_lst = lcl_4
                    _rbnf_immediate_lst.append(rbnf_tmp_0)
                    lcl_4 = _rbnf_immediate_lst
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = rbnf_named_lr_loop_Objects(rbnf_tmp_1_, builtin_state, builtin_tokens)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 2):
                lcl_3 = rbnf_named_parse_Script(builtin_state, builtin_tokens)
                rbnf_named__check_0 = lcl_3
                lcl_3 = rbnf_named__check_0[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_0
                else:
                    lcl_4 = rbnf_named__check_0[1]
                    rbnf_tmp_0 = lcl_4
                    lcl_4 = []
                    _rbnf_immediate_lst = lcl_4
                    _rbnf_immediate_lst.append(rbnf_tmp_0)
                    lcl_4 = _rbnf_immediate_lst
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = rbnf_named_lr_loop_Objects(rbnf_tmp_1_, builtin_state, builtin_tokens)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            else:
                lcl_3 = (rbnf_named__off_0, 'Objects lookahead failed')
                lcl_3 = builtin_cons(lcl_3, builtin_nil)
                lcl_3 = (False, lcl_3)
                lcl_1 = lcl_3
            lcl_0 = lcl_1
        else:
            lcl_1 = (rbnf_named__off_0, 'Objects got EOF')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_START(builtin_state, builtin_tokens):
        try:
            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
            if (_rbnf_cur_token.idint is 10):
                builtin_tokens.offset += 1
            else:
                _rbnf_cur_token = None
        except IndexError:
            _rbnf_cur_token = None
        lcl_0 = _rbnf_cur_token
        rbnf_tmp_0 = lcl_0
        lcl_0 = (rbnf_tmp_0 is None)
        if lcl_0:
            lcl_1 = builtin_tokens.offset
            lcl_1 = (lcl_1, 'BOF not match')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        else:
            lcl_1 = rbnf_named_parse_Objects(builtin_state, builtin_tokens)
            rbnf_named__check_1 = lcl_1
            lcl_1 = rbnf_named__check_1[0]
            lcl_1 = (lcl_1 == False)
            if lcl_1:
                lcl_1 = rbnf_named__check_1
            else:
                lcl_2 = rbnf_named__check_1[1]
                rbnf_tmp_1 = lcl_2
                try:
                    _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                    if (_rbnf_cur_token.idint is 11):
                        builtin_tokens.offset += 1
                    else:
                        _rbnf_cur_token = None
                except IndexError:
                    _rbnf_cur_token = None
                lcl_2 = _rbnf_cur_token
                rbnf_tmp_2 = lcl_2
                lcl_2 = (rbnf_tmp_2 is None)
                if lcl_2:
                    lcl_3 = builtin_tokens.offset
                    lcl_3 = (lcl_3, 'EOF not match')
                    lcl_3 = builtin_cons(lcl_3, builtin_nil)
                    lcl_3 = (False, lcl_3)
                    lcl_2 = lcl_3
                else:
                    lcl_3 = Seq(rbnf_tmp_1)
                    rbnf_tmp_1_ = lcl_3
                    lcl_3 = (True, rbnf_tmp_1_)
                    lcl_2 = lcl_3
                lcl_1 = lcl_2
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_Script(builtin_state, builtin_tokens):
        lcl_0 = rbnf_named_parse_Atom(builtin_state, builtin_tokens)
        rbnf_named__check_0 = lcl_0
        lcl_0 = rbnf_named__check_0[0]
        lcl_0 = (lcl_0 == False)
        if lcl_0:
            lcl_0 = rbnf_named__check_0
        else:
            lcl_1 = rbnf_named__check_0[1]
            rbnf_tmp_0 = lcl_1
            rbnf_tmp_1_ = rbnf_tmp_0
            lcl_1 = rbnf_named_lr_loop_Script(rbnf_tmp_1_, builtin_state, builtin_tokens)
            lcl_0 = lcl_1
        return lcl_0
    return rbnf_named_parse_START