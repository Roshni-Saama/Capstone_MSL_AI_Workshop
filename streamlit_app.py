"""Public Community Cloud entrypoint; local app.py retains local-only features."""
import os
from pathlib import Path
import runpy
import sys

os.environ["MSL_PUBLIC_DEMO"] = "1"
prototype = Path(__file__).resolve().parent / "prototype"
sys.path.insert(0, str(prototype))
runpy.run_path(str(prototype / "app.py"), run_name="__main__")
