import os
from pathlib import Path



desktop_path = Path.home() / 'Desktop'
desktop_os = os.path.join(os.path.expanduser('~'), 'Desktop')