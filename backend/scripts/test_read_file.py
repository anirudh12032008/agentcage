# quick testing gng

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.read_file import read_file
print("normal")
print(read_file("notes.txt"))

print("missing")
print(read_file("nope.txt"))

print("path traversal")
print(read_file("../main.py"))
print("abs path")
print(read_file("/etc/passwd"))