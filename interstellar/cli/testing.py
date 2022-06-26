import os
import threading
import subprocess

from cli.utils import create_dir, list_files, name_of, msg_of, insert_instead


def run_python(_py_file, _stdout=None, _stderr=True, _timeout=None):
    cmd = "python "
    if os.path.exists("./venv/Scripts/python.exe"):
        cmd = "./venv/Scripts/python.exe "
    cmd += _py_file

    try:
        proc = subprocess.run(cmd.split(), timeout=_timeout, capture_output=True)
    except subprocess.TimeoutExpired:
        if _stdout:
            timeouts_dir = insert_instead(_stdout, "timeouts")
            create_dir(timeouts_dir)
            timeout_dir = timeouts_dir + "/" + str(_timeout) + " secs"
            create_dir(timeout_dir)
            _stdout = timeout_dir + "/" + name_of(_stdout)
            file = open(_stdout.replace(".txt", ".timeout"), "w", encoding='utf-8')
            file.write("timeout... " + str(_timeout) + " sec(s)")
            file.close()
        return

    if _stdout:
        if proc.returncode == 0:
            file = open(_stdout, "w", encoding='utf-8')
            file.write(proc.stdout.decode('utf-8').replace("\r\n", "\n"))
        else:
            exceptions_dir = insert_instead(_stdout, "exceptions")
            create_dir(exceptions_dir)
            exception_dir = exceptions_dir + "/" + msg_of(proc.stderr.decode('utf-8'))
            create_dir(exception_dir)
            _stdout = exception_dir + "/" + name_of(_stdout)
            file = open(_stdout.replace(".txt", ".exception"), "w", encoding='utf-8')
            file.write(proc.stderr.decode('utf-8').replace("\r\n", "\n"))
        file.close()
    elif _stderr:
        print(proc.stderr.decode('utf-8'))

    return proc


def run_pythons(_py_dir):
    files = list_files(_py_dir)

    py_files = []
    for file in files:
        if ".py" in file:
            py_files.append(file)

    threads = []
    for py_file in py_files:
        t = threading.Thread(target=run_python, args=(_py_dir + py_file,), daemon=True)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()
