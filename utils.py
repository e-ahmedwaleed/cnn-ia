import os
import threading
import subprocess

DEBUG = False


def list_files(_dir):
    (_, _, files) = next(os.walk(_dir))
    return files


def msg_of(exception):
    return exception[exception.rfind(": ") + 2:].replace("\n", "")


def run_python(_py_file, _stdout=None, _stderr=True, _timeout=None):
    cmd = "python "
    if os.path.exists("./venv/Scripts/python.exe"):
        cmd = "./venv/Scripts/python.exe "
    cmd += _py_file

    if DEBUG:
        print(cmd)
        return

    try:
        proc = subprocess.run(cmd.split(), timeout=_timeout, capture_output=True)
    except subprocess.TimeoutExpired:
        if _stdout:
            file = open(_stdout.replace(".txt", ".timeout"), "w")
            file.write(str(_timeout) + " sec+")
            file.close()
        return

    if _stdout:
        if proc.returncode == 0:
            file = open(_stdout, "w")
            file.write(proc.stdout.decode('ascii'))
        else:
            # TODO: assertions should be handled in a special manner.
            file = open(_stdout.replace(".txt", ".exception"), "w")
            # msg_of(proc.stderr.decode('ascii'))
            file.write(proc.stderr.decode('ascii'))
        file.close()
    elif _stderr:
        print(proc.stderr.decode('ascii'))

    return proc


def run_pythons(_py_dir):
    files = list_files(_py_dir)

    py_files = []
    for file in files:
        if ".py" in file:
            py_files.append(file)

    threads = []
    for py_file in py_files:
        t = threading.Thread(target=run_python, args=(_py_dir + py_file,))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()


def list_samples(_type):
    samples = []
    samples_dir = "./interstellar/samples/" + _type + "/"
    for sample in list_files(samples_dir):
        if ".json" in sample:
            samples.append(samples_dir + sample)
    return samples


def name_of(file):
    return file[file.rfind("/") + 1:].replace(".json", "")


# noinspection SpellCheckingInspection
def run_interstellar_samples(_optimizer_type):
    layers = list_samples("layer")
    archs = list_samples("arch")
    schedules = list_samples("schedule")

    import random
    threads = []

    for i in range(10):
        layer = random.choice(layers)
        arch = random.choice(archs)
        schedule = random.choice(schedules)
        if _optimizer_type == "dataflow_explore":
            cmd = "./interstellar/main.py -v dataflow_explore " + arch + " " + layer
            output = "dataflow_explore-" + name_of(arch) + "-" + name_of(layer) + ".txt"
        else:
            cmd = "./interstellar/main.py -v -s " + schedule + " " + _optimizer_type + " " + arch + " " + layer
            output = _optimizer_type + "-" + name_of(schedule) + "-" + name_of(arch) + "-" + name_of(
                layer) + ".txt"

        t = threading.Thread(target=run_python, args=(cmd, "./output/" + output, False, 300,))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    return
