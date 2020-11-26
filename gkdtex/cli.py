from wisepy2 import wise
from gkdtex.interpreter import Interpreter
from pathlib import Path
import importlib.util
import gkdtex.builtins  # load builtin commands
import sys

def build(maintex_path: str, config_dir: str = '', out_file=''):
    if not config_dir:
        config_dir = '.'

    sys.path.append(config_dir)

    config_path = Path(config_dir) / ".gkdrc.py"

    if not out_file:
        out_file = str(Path(maintex_path).with_suffix('.out.tex'))

    if config_path.exists():
        spec = importlib.util.spec_from_file_location("gkd-main", str(config_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    interpreter = Interpreter()
    interpreter.initialize()

    Path(out_file).parent.mkdir(0o777, parents=True, exist_ok=True)

    with open(out_file, 'w') as f:
        interpreter.run_file(maintex_path, f.write)

    interpreter.dispose()

def main():
    wise(build)()
