import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# from utils.analysis_utils import analyze_interstellar_samples
from utils.python_utils import run_python, run_pythons, print_strikethrough  # , run_interstellar_samples

print("\nAvailable options:")
print("_________________\n")

print("(1) cnn-model parameters extractor")
print("(2) interstellar correctness tests")
print_strikethrough("(3) interstellar samples (loop blocking)")
print_strikethrough("(4) interstellar samples (memory capacity)")
print_strikethrough("(5) interstellar samples (dataflow exploration)")
print_strikethrough("(6) interstellar analyze samples (loop blocking)")
print_strikethrough("(7) interstellar analyze samples (memory capacity)")
print_strikethrough("(8) interstellar analyze samples (dataflow exploration)")

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
    pass  # run_interstellar_samples("basic")
elif choice == 4:
    pass  # run_interstellar_samples("mem_explore")
elif choice == 5:
    pass  # run_interstellar_samples("dataflow_explore")
elif choice == 6:
    pass  # analyze_interstellar_samples("loop-blocking")
elif choice == 7:
    pass  # analyze_interstellar_samples("memory-capacity")
elif choice == 8:
    pass  # analyze_interstellar_samples("dataflow")
