from pathlib import Path
import sys
src_path = Path(__file__).parent/"../src"
sys.path.append(str(src_path))

# pylint: disable=import-error
import pyASBC
