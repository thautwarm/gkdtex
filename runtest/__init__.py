from gkdtex.wrap import parse
from gkdtex.interpreter import Interpreter, CBVFunction
import sys

src = r"""

\newcommand{\GKDCreateId}{\input{|"gkdmgr --op uuid --rt A"}}

\makeatletter
\newcommand*\GKDNewTemp[2]{
  \@ifundefined{GKDTemp#1}{
    \expandafter\newcommand\csname GKDTemp#1\endcsname{#2}
  }{
    \expandafter\renewcommand\csname GKDTemp#1\endcsname{#2}
  }
}
\makeatother

\GKDNewTemp{ConstID}{\GKDCreateId}

\newcommand{\GKDSet}[2]{\input{|"gkdmgr --op set --rt \GKDTempConstID #1 #2"}}
\newcommand{\GKDGet}[1]{\input{|"gkdmgr --op get --rt \GKDTempConstID #1"}}
\newcommand{\GKDPush}[2]{\input{|"gkdmgr --op push --rt \GKDTempConstID  #1 #2"}}
\newcommand{\GKDPop}[1]{\input{|"gkdmgr --op pop --rt \GKDTempConstID #1"}}
\newcommand{\GKDPyCall}[2]{\input{|"gkdmgr --op call --rt \GKDTempConstID #1 #2"}}



\makeatletter
\newenvironment{GKDBNF}[1]
  {\VerbatimEnvironment
    \GKDNewTemp{A}{#1}
    \input{|"gkdmgr --op createDirFor --rt any ./gkdbnf/#1.bnf"}
    \VerbatimOut{./gkdbnf/#1.bnf}
  }%
  {%
    \endVerbatimOut%
    \toks0{\immediate\write18}%
    
    \begin{bnf*}
      \input{|"gkdmgr --op bnf --rt any ./gkdbnf/\GKDTempA.bnf"}%
    \end{bnf*}
   
  }
\verb{a}
\makeatother
"""


body = parse(r"""$ #\1^{ #\1#1 } $""")

interpreter = Interpreter()
interpreter.filename = "a.tex"
interpreter.src = src
interpreter.globals['mk'] = CBVFunction([""], [None], dict(d=0), body)


def verb(self: Interpreter, spans, tex_print, _):
    span = spans[0]
    src = span.src
    l, r = span.offs
    tex_print('<<')
    tex_print(src[l:r])
    tex_print('>>')

interpreter.globals['verb'] = verb
interpreter.interp(sys.stdout.write, parse(src, "a.tex"))
