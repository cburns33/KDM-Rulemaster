"""Save final affected-case validation separately from earlier development runs."""
from pathlib import Path

import run

if __name__ == '__main__':
    run.OUT = Path(__file__).resolve().parent / 'final'
    run.OUT.mkdir(exist_ok=True)
    run.main()
