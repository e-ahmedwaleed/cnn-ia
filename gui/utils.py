import os
import subprocess

main_dir_path = os.path.dirname(os.path.abspath("main.py")).replace("\\", "/")


def sleep(_seconds):
    import time
    time.sleep(_seconds)


def run_command(_cmd):
    proc = subprocess.run(_cmd.split(), capture_output=True)
    print(proc.stdout.decode('ascii'))
    print(proc.stderr.decode('ascii'))
    return proc


def run_subprocess(_args):
    cmd = "python "
    if os.path.exists("./venv/Scripts/python.exe"):
        cmd = "./venv/Scripts/python.exe "

    cmd += _args
    return subprocess.Popen(cmd.split())


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
    from PyQt5.QtWidgets import QFileDialog
    return QFileDialog.getExistingDirectory(parent=None, caption=_caption, directory=main_dir_path)
