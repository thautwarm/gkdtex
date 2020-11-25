from wisepy2 import wise
from gkdtex.builtins import interpreter
from pathlib import Path
import importlib.util

def build(maintex_path: str, config_path: str = '', out_file=''):
    if not config_path:
        config_path = ".gkdrc.py"

    if not Path(out_file).exists():
        out_file = Path(maintex_path).with_suffix('.out.tex')

    if Path(config_path).exists():
        spec = importlib.util.spec_from_file_location("gkd-main", config_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    interpreter.initialize()

    Path(out_file).parent.mkdir(0o777, parents=True, exist_ok=True)
    with open(out_file, 'w') as f:
        interpreter.run_file(maintex_path, f.write)

def main():
    wise(build)()
