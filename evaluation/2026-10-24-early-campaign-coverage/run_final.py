"""Save the scope repair validation without changing the first run."""
from pathlib import Path
import run

if __name__ == '__main__':
    run.OUT = Path(__file__).resolve().parent / 'final'
    run.OUT.mkdir(exist_ok=True)
    run.CASES.append(('N17', 'Now a standard level 1 White Lion, not the Prologue. Do we copy the deployment and fixed deck?', 'white-lion-deployment', True))
    run.main()
