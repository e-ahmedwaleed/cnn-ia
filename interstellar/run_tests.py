import os
import sys
import threading
import subprocess

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


def list_files(_dir):
    (_, _, files) = next(os.walk(_dir))
    return files


def run_python(_py_file):
    subprocess.run(("python " + _py_file).split())


_py_dir = file_dir + "/test-correctness/"

py_files = []
for file in list_files(_py_dir):
    if ".py" in file:
        py_files.append(file)

threads = []
for py_file in py_files:
    t = threading.Thread(target=run_python, args=(_py_dir + py_file,))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()
