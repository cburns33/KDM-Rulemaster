"""Open an existing instance or start the app in this console."""
import json
import subprocess
import sys
import urllib.request
import webbrowser
from pathlib import Path

url = 'http://127.0.0.1:8765'
try:
    with urllib.request.urlopen(url + '/api/health', timeout=2) as response:
        state = json.load(response)
    if state.get('app') == 'lantern-archive':
        webbrowser.open(url)
    else:
        raise RuntimeError('Another application is using port 8765. Run server.py --port 8766 --open.')
except (OSError, TimeoutError):
    subprocess.run([sys.executable, 'server.py', '--open'], cwd=Path(__file__).resolve().parent, check=True)
