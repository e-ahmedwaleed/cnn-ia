import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from utils.python_utils import run_python, run_pythons, run_interstellar_samples
from utils.analysis_utils import analyze_interstellar_samples

print("\nAvailable options:")
print("_________________\n")

print("(1) cnn-model parameters extractor")
print("(2) interstellar correctness tests")
print("(3) interstellar samples (loop blocking)")
print("(4) interstellar samples (memory capacity)")
print("(5) interstellar samples (dataflow exploration)")
print("(6) interstellar analyze samples (loop blocking)")
print("(7) interstellar analyze samples (memory capacity)")
print("(8) interstellar analyze samples (dataflow exploration)")

print("\n(9) exit\n")

choice = 0

while True:
    try:
        choice = int(input("Enter your choice (1-9): ")[0])
        if (1 <= choice) & (choice <= 9):
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
elif choice == 6:
    analyze_interstellar_samples("loop-blocking")
elif choice == 7:
    analyze_interstellar_samples("memory-capacity")
elif choice == 8:
    analyze_interstellar_samples("dataflow")
