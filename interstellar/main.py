import os
import threading
import subprocess

DEBUG = False
TIMEOUT = 10


def list_files(_dir):
    (_, _, files) = next(os.walk(_dir))
    return files


def create_dir(_path):
    try:
        os.mkdir(_path)
        return True
    except OSError:
        return False


def insert_instead(_file, _folder):
    return _file[0:_file.rfind("/")] + "/" + _folder


def name_of(_file):
    return _file[_file.rfind("/") + 1:].replace(".json", "")


def msg_of(_exception):
    return _exception[_exception.rfind(": ") + 2:].replace(".", "").replace("\n", "").replace("\r", "")


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
        t = threading.Thread(target=run_python, args=(_py_dir + py_file,))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()


def list_samples(_type):
    samples = []
    samples_dir = "./samples/" + _type + "/"
    for sample in list_files(samples_dir):
        if ".json" in sample:
            samples.append(samples_dir + sample)
    return samples


# noinspection SpellCheckingInspection
def run_interstellar_samples(_optimizer_type):
    layers = list_samples("layer")
    archs = list_samples("arch")
    schedules = list_samples("schedule")

    output_dir = "interstellar_output"
    create_dir(output_dir)

    optimizer_dir = output_dir + "/"
    if _optimizer_type == "basic":
        optimizer_dir += "loop-blocking"
    else:
        optimizer_dir += "dataflow"
    create_dir(optimizer_dir)

    for layer in layers:
        layer_dir = optimizer_dir + "/" + name_of(layer)
        create_dir(layer_dir)
        threads = []
        for arch in archs:
            arch_dir = layer_dir + "/" + name_of(arch)
            if _optimizer_type == "dataflow_explore":
                cmd = "./run_optimizer.py -v dataflow_explore " + arch + " " + layer
                output = arch_dir + ".txt"

                t = threading.Thread(target=run_python, args=(cmd, output, False, TIMEOUT,))
                threads.append(t)
                t.start()
            else:
                threads = []
                create_dir(arch_dir)
                for schedule in schedules:
                    schedule_file = arch_dir + "/" + name_of(schedule)
                    cmd = "./run_optimizer.py -v -s " + schedule + " " + _optimizer_type + " " + arch + " " + layer
                    output = schedule_file + ".txt"

                    t = threading.Thread(target=run_python, args=(cmd, output, False, TIMEOUT,))
                    threads.append(t)
                    t.start()

                for schedule_thread in threads:
                    schedule_thread.join()
                if DEBUG:
                    return

        for arch_thread in threads:
            arch_thread.join()
        if DEBUG:
            return

    return


print("\nAvailable options:")
print("_________________\n")

print("(1) interstellar correctness tests")
print("(2) interstellar samples (dataflow exploration)")

print("\n(0) exit\n")

choice = 0

while True:
    try:
        choice = int(input("Enter your choice (0-2): ")[0])
        if choice <= 2:
            break
    except ValueError:
        continue
    except IndexError:
        continue

if choice == 1:
    run_pythons("./test_correctness/")
elif choice == 2:
    run_interstellar_samples("dataflow_explore")
