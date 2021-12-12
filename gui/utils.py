import os

main_dir_path = os.path.dirname(os.path.abspath("main.py")).replace("\\", "/")


def sleep(_seconds):
    import time
    time.sleep(_seconds)


def run_command(_cmd):
    import subprocess
    proc = subprocess.run(_cmd.split(), capture_output=True)
    print(proc.stdout.decode('ascii'))
    print(proc.stderr.decode('ascii'))
    return proc


def create_folder(_path):
    import os
    try:
        os.mkdir(_path)
        return True
    except OSError:
        return False


def open_folder(_path):
    import subprocess
    subprocess.Popen(r'explorer /select,"' + str(_path).replace('/', '\\') + '"')


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
