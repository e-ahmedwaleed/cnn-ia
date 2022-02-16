import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from utils import run_python, run_pythons, run_interstellar_samples

print("\nAvailable options:")
print("_________________\n")

print("(1) cnn-model parameters extractor")
print("(2) interstellar correctness tests")
print("(3) interstellar samples (loop blocking)")
print("(4) interstellar samples (memory capacity)")
print("(5) interstellar samples (dataflow exploration)")

print("\n(0) exit\n")

choice = 0

while True:
    try:
        choice = int(input("Enter your choice (0-5): ")[0])
        if choice <= 5:
            break
    except ValueError:
        continue
    except IndexError:
        continue

if choice == 1:
    run_python("./phase-1-extractor/main.py")
elif choice == 2:
    run_pythons("./interstellar/test-correctness/")
elif choice == 3:
    run_interstellar_samples("basic")
elif choice == 4:
    run_interstellar_samples("mem_explore")
elif choice == 5:
    run_interstellar_samples("dataflow_explore")
