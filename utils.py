import os
import threading
import subprocess


def run_python(_py_file, _stdout=False, _stderr=True):
    _cmd = "python "
    if os.path.exists("./venv/Scripts/python.exe"):
        _cmd = "./venv/Scripts/python.exe "

    _cmd += _py_file
    _proc = subprocess.run(_cmd.split(), capture_output=True)
    if _stdout:
        print(_proc.stdout.decode('ascii'))
    if _stderr:
        print(_proc.stderr.decode('ascii'))
    return _proc


def run_pythons(_py_dir):
    (_, _, files) = next(os.walk(_py_dir))

    _py_files = []
    for file in files:
        if ".py" in file:
            _py_files.append(file)

    threads = []
    for _py_file in _py_files:
        t = threading.Thread(target=run_python, args=(_py_dir + _py_file,))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()
