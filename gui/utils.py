import os

dirty_semaphore = ''
main_dir_path = os.path.dirname(os.path.abspath("main.py")).replace("\\", "/")


def natural_sort(_unsorted):
    import re
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split(r'(\d+)', key)]
    return sorted(_unsorted, key=alphanum_key)


def sleep(_seconds):
    import time
    time.sleep(_seconds)


def run_python(_args):
    import subprocess

    cmd = "python "

    if os.path.exists("./venv/Scripts/python.exe"):
        cmd = "./venv/Scripts/python.exe "
    elif main_dir_path[0] == '/':
        cmd = "python3 "

    cmd += _args

    proc = subprocess.run(cmd.split(), capture_output=True)
    print(proc.stdout.decode('ascii'))
    print(proc.stderr.decode('ascii'))
    return proc


def run_python_subprocess(_args):
    import subprocess

    cmd = "python "

    if os.path.exists("./venv/Scripts/python.exe"):
        cmd = "./venv/Scripts/python.exe "
    elif main_dir_path[0] == '/':
        cmd = "python3 "

    cmd += _args
    return subprocess.Popen(cmd.split())


def list_files(_dir):
    (_, _, files) = next(os.walk(_dir))
    return files


def create_file(_path, _content):
    file = open(_path, "w")
    file.write(_content)
    file.close()


def create_folder(_path):
    try:
        os.mkdir(_path)
        return True
    except OSError:
        return False


def delete_folder(_path):
    import shutil
    try:
        shutil.rmtree(_path)
        return True
    except OSError:
        return False


def choose_file_dialog(_caption, _filter):
    from PyQt5.QtWidgets import QFileDialog
    return QFileDialog.getOpenFileName(parent=None, caption=_caption, directory=main_dir_path, filter=_filter)[0]


def choose_folder_dialog(_caption):
    if main_dir_path[0] == '/':
        return main_dir_path
    from PyQt5.QtWidgets import QFileDialog
    return QFileDialog.getExistingDirectory(parent=None, caption=_caption, directory=main_dir_path)


def acquire_dirty_semaphore():
    create_file(dirty_semaphore, ' ')


def check_dirty_semaphore(_path):
    return os.path.exists(_path.replace('*', ' ').replace(".onnx", ".temp"))


def release_dirty_semaphore():
    os.remove(dirty_semaphore)
    import netron
    netron.stop()
    print("You should not see me...")
