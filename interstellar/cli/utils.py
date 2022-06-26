import os
import sys


def read_int(message, l_limit=~sys.maxsize, u_limit=sys.maxsize):
    while True:
        try:
            num = int(input(message))
            if (l_limit <= num) & (num <= u_limit):
                return num
        except ValueError:
            continue
        except IndexError:
            continue


def create_dir(_path):
    try:
        os.mkdir(_path)
        return True
    except OSError:
        return False


# dir_path/ -> ['file0', 'file1', ...]
def list_files(_dir):
    (_, _, files) = next(os.walk(_dir))
    return files


# dir_path/ -> ['dir0', 'dir1', ...]
def list_dirs(_dir):
    (_, dirs, _) = next(os.walk(_dir))
    return dirs


# file_path/file_name.txt & _dir_name -> file_path/_dir_name
def insert_instead(_file, _dir):
    return _file[0:_file.rfind("/")] + "/" + _dir


# file_path/file_name.json -> file_name
def name_of(_file):
    return _file[_file.rfind("/") + 1:].replace(".json", "")


# traceback (most recent call last): ... [error:] exception_msg. -> exception_msg
def msg_of(_exception):
    last_line = _exception.splitlines()[-1]
    return last_line[last_line.rfind(": ") + 1:].strip().replace('.', '')
