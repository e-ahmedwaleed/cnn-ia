import os.path
import subprocess

print("\nAvailable options:")
print("_________________\n")

print("(1) cnn-model parameters extractor")
print("(2) interstellar correctness tests")

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


if choice == 1:
    print(run_python("./phase-1-extractor/main.py").returncode == 0)
elif choice == 2:
    from os import walk

    (_, _, filenames) = next(walk("./interstellar/test-correctness/"))
    test_files = filenames[1:]

    tests = []
    for test_file in test_files:
        import threading

        t = threading.Thread(target=run_python, args=("./interstellar/test-correctness/" + test_file,))
        tests.append(t)
        t.start()

    for test in tests:
        test.join()
