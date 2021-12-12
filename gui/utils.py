import os

main_dir_path = os.path.dirname(os.path.abspath("main.py")).replace("\\", "/")


def choose_file_dialog(_caption, _filter):
    from PyQt5.QtWidgets import QFileDialog
    return QFileDialog.getOpenFileName(parent=None, caption=_caption, directory=main_dir_path, filter=_filter)[0]


def choose_folder_dialog(_caption):
    from PyQt5.QtWidgets import QFileDialog
    return QFileDialog.getExistingDirectory(parent=None, caption=_caption, directory=main_dir_path)


def create_folder(_path):
    import os
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


def run_command(_cmd):
    import subprocess
    proc = subprocess.run(_cmd.split(), capture_output=True)
    print(proc.stdout.decode('ascii'))
    print(proc.stderr.decode('ascii'))
    return proc
